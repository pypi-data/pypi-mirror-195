import os
import random
import uuid
from time import time
from urllib import request

import torch
import torch.nn.functional as F
import progressbar
import torchaudio

from ruth_tts_transformer.models.classifier import AudioMiniEncoderWithClassifierHead
from ruth_tts_transformer.models.diffusion_decoder import DiffusionTts
from ruth_tts_transformer.models.autoregressive import UnifiedVoice
from tqdm import tqdm

from ruth_tts_transformer.models.arch_util import TorchMelSpectrogram
from ruth_tts_transformer.models.clvp import CLVP
from ruth_tts_transformer.models.random_latent_generator import RandomLatentConverter
from ruth_tts_transformer.models.vocoder import UnivNetGenerator
from ruth_tts_transformer.utils.audio import wav_to_univnet_mel, denormalize_tacotron_mel
from ruth_tts_transformer.utils.diffusion import SpacedDiffusion, space_timesteps, get_named_beta_schedule
from ruth_tts_transformer.utils.tokenizer import VoiceBpeTokenizer
from ruth_tts_transformer.utils.wav2vec_alignment import Wav2VecAlignment

pbar = None

DEFAULT_MODELS_DIR = os.path.join(os.path.expanduser('~'), '.cache', 'tortoise', 'models')
MODELS_DIR = os.environ.get('TORTOISE_MODELS_DIR', DEFAULT_MODELS_DIR)
MODELS = {
    'autoregressive.pth': 'https://huggingface.co/PuretalkMeca/ruth-tts/resolve/main/gpt.pth',
    'clvp2.pth': 'https://huggingface.co/PuretalkMeca/ruth-tts/resolve/main/best_sample.pth',
    'diffusion_decoder.pth': 'https://huggingface.co/PuretalkMeca/ruth-tts/resolve/main/best_sample.pth',
    'vocoder.pth': 'https://huggingface.co/PuretalkMeca/ruth-tts/blob/main/univ_c16_0292.pth',
}


def download_models(specific_models=None):
    """
    Call to download all the models that Tortoise uses.
    """
    os.makedirs(MODELS_DIR, exist_ok=True)

    def show_progress(block_num, block_size, total_size):
        global pbar
        if pbar is None:
            pbar = progressbar.ProgressBar(maxval=total_size)
            pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            pbar.update(downloaded)
        else:
            pbar.finish()
            pbar = None

    for model_name, url in MODELS.items():
        if specific_models is not None and model_name not in specific_models:
            continue
        model_path = os.path.join(MODELS_DIR, model_name)
        if os.path.exists(model_path):
            continue

        request.urlretrieve(url, model_path, show_progress)


def get_model_path(model_name, models_dir=MODELS_DIR):
    """
    Get path to given model, download it if it doesn't exist.
    """
    if model_name not in MODELS:
        raise ValueError(f'Model {model_name} not found in available models.')
    model_path = os.path.join(models_dir, model_name)
    if not os.path.exists(model_path) and models_dir == MODELS_DIR:
        download_models([model_name])
    return model_path


def pad_or_truncate(t, length):
    """
    Utility function for forcing <t> to have the specified sequence length, whether by clipping it or padding it with 0s.
    """
    if t.shape[-1] == length:
        return t
    elif t.shape[-1] < length:
        return F.pad(t, (0, length - t.shape[-1]))
    else:
        return t[..., :length]


def load_discrete_vocoder_diffuser(trained_diffusion_steps=4000, desired_diffusion_steps=200, cond_free=True,
                                   cond_free_k=1):
    """
    Helper function to load a GaussianDiffusion instance configured for use as a vocoder.
    """
    return SpacedDiffusion(use_timesteps=space_timesteps(trained_diffusion_steps, [desired_diffusion_steps]),
                           model_mean_type='epsilon',
                           model_var_type='learned_range', loss_type='mse',
                           betas=get_named_beta_schedule('linear', trained_diffusion_steps),
                           conditioning_free=cond_free, conditioning_free_k=cond_free_k)


def format_conditioning(clip, cond_length=132300, device='cuda'):
    """
    Converts the given conditioning signal to a MEL spectrogram and clips it as expected by the models.
    """
    gap = clip.shape[-1] - cond_length
    if gap < 0:
        clip = F.pad(clip, pad=(0, abs(gap)))
    elif gap > 0:
        rand_start = random.randint(0, gap)
        clip = clip[:, rand_start:rand_start + cond_length]
    mel_clip = TorchMelSpectrogram()(clip.unsqueeze(0)).squeeze(0)
    return mel_clip.unsqueeze(0).to(device)


def fix_autoregressive_output(codes, stop_token, complain=True):
    """
    This function performs some padding on coded audio that fixes a mismatch issue between what the diffusion model was
    trained on and what the autoregressive code generator creates (which has no padding or end).
    This is highly specific to the DVAE being used, so this particular coding will not necessarily work if used with
    a different DVAE. This can be inferred by feeding a audio clip padded with lots of zeros on the end through the DVAE
    and copying out the last few codes.

    Failing to do this padding will produce speech with a harsh end that sounds like "BLAH" or similar.
    """
    # Strip off the autoregressive stop token and add padding.
    stop_token_indices = (codes == stop_token).nonzero()
    if len(stop_token_indices) == 0:
        if complain:
            print("No stop tokens found in one of the generated voice clips. This typically means the spoken audio is "
                  "too long. In some cases, the output will still be good, though. Listen to it and if it is missing words, "
                  "try breaking up your input text.")
        return codes
    else:
        codes[stop_token_indices] = 83
    stm = stop_token_indices.min().item()
    codes[stm:] = 83
    if stm - 3 < codes.shape[0]:
        codes[-3] = 45
        codes[-2] = 45
        codes[-1] = 248

    return codes


def do_spectrogram_diffusion(diffusion_model, diffuser, latents, conditioning_latents, temperature=1, verbose=True):
    """
    Uses the specified diffusion model to convert discrete codes into a spectrogram.
    """
    with torch.no_grad():
        output_seq_len = latents.shape[
                             1] * 4 * 24000 // 22050  # This diffusion model converts from 22kHz spectrogram codes to a 24kHz spectrogram signal.
        output_shape = (latents.shape[0], 100, output_seq_len)
        precomputed_embeddings = diffusion_model.timestep_independent(latents, conditioning_latents, output_seq_len,
                                                                      False)

        noise = torch.randn(output_shape, device=latents.device) * temperature
        mel = diffuser.p_sample_loop(diffusion_model, output_shape, noise=noise,
                                     model_kwargs={'precomputed_aligned_embeddings': precomputed_embeddings},
                                     progress=verbose)
        return denormalize_tacotron_mel(mel)[:, :, :output_seq_len]


def classify_audio_clip(clip):
    """
    Returns whether or not Tortoises' classifier thinks the given clip came from Tortoise.
    :param clip: torch tensor containing audio waveform data (get it from load_audio)
    :return: True if the clip was classified as coming from Tortoise and false if it was classified as real.
    """
    classifier = AudioMiniEncoderWithClassifierHead(2, spec_dim=1, embedding_dim=512, depth=5, downsample_factor=4,
                                                    resnet_blocks=2, attn_blocks=4, num_attn_heads=4, base_channels=32,
                                                    dropout=0, kernel_size=5, distribute_zero_label=False)
    classifier.load_state_dict(torch.load(get_model_path('classifier.pth'), map_location=torch.device('cpu')))
    clip = clip.cpu().unsqueeze(0)
    results = F.softmax(classifier(clip), dim=-1)
    return results[0][0]


def pick_best_batch_size_for_gpu():
    """
    Tries to pick a batch size that will fit in your GPU. These sizes aren't guaranteed to work, but they should give
    you a good shot.
    """
    if torch.cuda.is_available():
        _, available = torch.cuda.mem_get_info()
        availableGb = available / (1024 ** 3)
        if availableGb > 14:
            return 16
        elif availableGb > 10:
            return 8
        elif availableGb > 7:
            return 4
    return 1


class TextToSpeech:
    """
    Main entry point into Tortoise.
    """

    def __init__(self, voice="gabby", autoregressive_batch_size=None, models_dir=MODELS_DIR, enable_redaction=True, device=None):
        # """
        # Constructor
        # :param autoregressive_batch_size: Specifies how many samples to generate per batch. Lower this if you are seeing
        #                                   GPU OOM errors. Larger numbers generates slightly faster.
        # :param models_dir: Where model weights are stored. This should only be specified if you are providing your own
        #                    models, otherwise use the defaults.
        # :param enable_redaction: When true, text enclosed in brackets are automatically redacted from the spoken output
        #                          (but are still rendered by the model). This can be used for prompt engineering.
        #                          Default is true.
        # :param device: Device to use when running the model. If omitted, the device will be automatically chosen.
        # """
        self.voice = voice
        self.models_dir = models_dir
        self.autoregressive_batch_size = pick_best_batch_size_for_gpu() if autoregressive_batch_size is None else autoregressive_batch_size
        self.enable_redaction = enable_redaction
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if self.enable_redaction:
            self.aligner = Wav2VecAlignment()

        self.tokenizer = VoiceBpeTokenizer()

        if os.path.exists(f'{models_dir}/autoregressive.ptt'):
            # Assume this is a traced directory.
            self.autoregressive = torch.jit.load(f'{models_dir}/autoregressive.ptt')
            self.diffusion = torch.jit.load(f'{models_dir}/diffusion_decoder.ptt')
        else:
            self.autoregressive = UnifiedVoice(max_mel_tokens=604, max_text_tokens=402, max_conditioning_inputs=2,
                                               layers=30,
                                               model_dim=1024,
                                               heads=16, number_text_tokens=255, start_text_token=255,
                                               checkpointing=False,
                                               train_solo_embeddings=False).cpu().eval()
            self.autoregressive.load_state_dict(torch.load(get_model_path('autoregressive.pth', models_dir)))

            self.diffusion = DiffusionTts(model_channels=1024, num_layers=10, in_channels=100, out_channels=200,
                                          in_latent_channels=1024, in_tokens=8193, dropout=0, use_fp16=False,
                                          num_heads=16,
                                          layer_drop=0, unconditioned_percentage=0).cpu().eval()
            self.diffusion.load_state_dict(torch.load(get_model_path('diffusion_decoder.pth', models_dir)))

        self.clvp = CLVP(dim_text=768, dim_speech=768, dim_latent=768, num_text_tokens=256, text_enc_depth=20,
                         text_seq_len=350, text_heads=12,
                         num_speech_tokens=8192, speech_enc_depth=20, speech_heads=12, speech_seq_len=430,
                         use_xformers=True).cpu().eval()
        self.clvp.load_state_dict(torch.load(get_model_path('clvp2.pth', models_dir)))

        self.vocoder = UnivNetGenerator().cpu()
        self.vocoder.load_state_dict(
            torch.load(get_model_path('vocoder.pth', models_dir), map_location=torch.device('cpu'))['model_g'])
        self.vocoder.eval(inference=True)

        # Random latent generators (RLGs) are loaded lazily.
        self.rlg_auto = None
        self.rlg_diffusion = None

    def get_conditioning_latents(self, voice_samples, return_mels=False):
        """
        Transforms one or more voice_samples into a tuple (autoregressive_conditioning_latent, diffusion_conditioning_latent).
        These are expressive learned latents that encode aspects of the provided clips like voice, intonation, and acoustic
        properties.
        :param voice_samples: List of 2 or more ~10 second reference clips, which should be torch tensors containing 22.05kHz waveform data.
        """
        with torch.no_grad():
            voice_samples = [v.to(self.device) for v in voice_samples]

            auto_conds = []
            if not isinstance(voice_samples, list):
                voice_samples = [voice_samples]
            for vs in voice_samples:
                auto_conds.append(format_conditioning(vs, device=self.device))
            auto_conds = torch.stack(auto_conds, dim=1)
            self.autoregressive = self.autoregressive.to(self.device)
            auto_latent = self.autoregressive.get_conditioning(auto_conds)
            self.autoregressive = self.autoregressive.cpu()

            diffusion_conds = []
            for sample in voice_samples:
                # The diffuser operates at a sample rate of 24000 (except for the latent inputs)
                sample = torchaudio.functional.resample(sample, 22050, 24000)
                sample = pad_or_truncate(sample, 102400)
                cond_mel = wav_to_univnet_mel(sample.to(self.device), do_normalization=False, device=self.device)
                diffusion_conds.append(cond_mel)
            diffusion_conds = torch.stack(diffusion_conds, dim=1)

            self.diffusion = self.diffusion.to(self.device)
            diffusion_latent = self.diffusion.get_conditioning(diffusion_conds)
            self.diffusion = self.diffusion.cpu()

        if return_mels:
            return auto_latent, diffusion_latent, auto_conds, diffusion_conds
        else:
            return auto_latent, diffusion_latent

    def get_random_conditioning_latents(self):
        # Lazy-load the RLG models.
        if self.rlg_auto is None:
            self.rlg_auto = RandomLatentConverter(1024).eval()
            self.rlg_auto.load_state_dict(
                torch.load(get_model_path('rlg_auto.pth', self.models_dir), map_location=torch.device('cpu')))
            self.rlg_diffusion = RandomLatentConverter(2048).eval()
            self.rlg_diffusion.load_state_dict(
                torch.load(get_model_path('rlg_diffuser.pth', self.models_dir), map_location=torch.device('cpu')))
        with torch.no_grad():
            return self.rlg_auto(torch.tensor([0.0])), self.rlg_diffusion(torch.tensor([0.0]))

    def tts_with_preset(self, text, preset='fast', **kwargs):
        """
        Calls TTS with one of a set of preset generation parameters. Options:
            'ultra_fast': Produces speech at a speed which belies the name of this repo. (Not really, but it's definitely fastest).
            'fast': Decent quality speech at a decent inference rate. A good choice for mass inference.
            'standard': Very good quality. This is generally about as good as you are going to get.
            'high_quality': Use if you want the absolute best. This is not really worth the compute, though.
        """
        # Use generally found best tuning knobs for generation.
        settings = {'temperature': .8, 'length_penalty': 1.0, 'repetition_penalty': 2.0,
                    'top_p': .8,
                    'cond_free_k': 2.0, 'diffusion_temperature': 1.0}
        # Presets are defined here.
        presets = {
            'ultra_fast': {'num_autoregressive_samples': 16, 'diffusion_iterations': 30, 'cond_free': False},
            'fast': {'num_autoregressive_samples': 96, 'diffusion_iterations': 80},
            'standard': {'num_autoregressive_samples': 256, 'diffusion_iterations': 200},
            'high_quality': {'num_autoregressive_samples': 256, 'diffusion_iterations': 400},
        }
        settings.update(presets[preset])
        settings.update(kwargs)  # allow overriding of preset settings with kwargs
        return self.tts(text, **settings)

    def tts(self, text, voice_samples=None, conditioning_latents=None, k=1, verbose=True, use_deterministic_seed=None,
            return_deterministic_state=False,
            # autoregressive generation parameters follow
            num_autoregressive_samples=512, temperature=.8, length_penalty=1, repetition_penalty=2.0, top_p=.8,
            max_mel_tokens=500,
            # diffusion generation parameters follow
            diffusion_iterations=100, cond_free=True, cond_free_k=2, diffusion_temperature=1.0,
            **hf_generate_kwargs):
        self.text = text
        deterministic_seed = self.deterministic_state(seed=use_deterministic_seed)

        text_tokens = torch.IntTensor(self.tokenizer.encode(text)).unsqueeze(0).to(self.device)
        text_tokens = F.pad(text_tokens, (0, 1))  # This may not be necessary.
        assert text_tokens.shape[
                   -1] < 400, 'Too much text provided. Break the text up into separate segments and re-try inference.'

        auto_conds = None
        if voice_samples is not None:
            auto_conditioning, diffusion_conditioning, auto_conds, _ = self.get_conditioning_latents(voice_samples,
                                                                                                     return_mels=True)
        elif conditioning_latents is not None:
            auto_conditioning, diffusion_conditioning = conditioning_latents
        else:
            auto_conditioning, diffusion_conditioning = self.get_random_conditioning_latents()
        auto_conditioning = auto_conditioning.to(self.device)
        diffusion_conditioning = diffusion_conditioning.to(self.device)

        diffuser = load_discrete_vocoder_diffuser(desired_diffusion_steps=diffusion_iterations, cond_free=cond_free,
                                                  cond_free_k=cond_free_k)

        with torch.no_grad():
            samples = []
            num_batches = num_autoregressive_samples // self.autoregressive_batch_size
            stop_mel_token = self.autoregressive.stop_mel_token
            calm_token = 83  # This is the token for coding silence, which is fixed in place with "fix_autoregressive_output"
            self.autoregressive = self.autoregressive.to(self.device)
            if verbose:
                print("Generating autoregressive samples..")
            for b in tqdm(range(num_batches), disable=not verbose):
                codes = self.autoregressive.inference_speech(auto_conditioning, text_tokens,
                                                             do_sample=True,
                                                             top_p=top_p,
                                                             temperature=temperature,
                                                             num_return_sequences=self.autoregressive_batch_size,
                                                             length_penalty=length_penalty,
                                                             repetition_penalty=repetition_penalty,
                                                             max_generate_length=max_mel_tokens,
                                                             **hf_generate_kwargs)
                padding_needed = max_mel_tokens - codes.shape[1]
                codes = F.pad(codes, (0, padding_needed), value=stop_mel_token)
                samples.append(codes)
            self.autoregressive = self.autoregressive.cpu()

            clip_results = []

            if verbose:
                print("Computing best candidates using CLVP")

            for batch in tqdm(samples, disable=not verbose):
                for i in range(batch.shape[0]):
                    batch[i] = fix_autoregressive_output(batch[i], stop_mel_token)

                clvp = self.clvp(text_tokens.repeat(batch.shape[0], 1), batch, return_loss=False)
                clip_results.append(clvp)

            clip_results = torch.cat(clip_results, dim=0)
            samples = torch.cat(samples, dim=0)
            best_results = samples[torch.topk(clip_results, k=k).indices]
            self.clvp = self.clvp.cpu()

            del samples

            # The diffusion model actually wants the last hidden layer from the autoregressive model as conditioning
            # inputs. Re-produce those for the top results. This could be made more efficient by storing all of these
            # results, but will increase memory usage.
            self.autoregressive = self.autoregressive.to(self.device)
            best_latents = self.autoregressive(auto_conditioning.repeat(k, 1), text_tokens.repeat(k, 1),
                                               torch.tensor([text_tokens.shape[-1]], device=text_tokens.device),
                                               best_results,
                                               torch.tensor([best_results.shape[
                                                                 -1] * self.autoregressive.mel_length_compression],
                                                            device=text_tokens.device),
                                               return_latent=True, clip_inputs=False)
            self.autoregressive = self.autoregressive.cpu()
            del auto_conditioning

            if verbose:
                print("Transforming autoregressive outputs into audio..")
            wav_candidates = []
            self.diffusion = self.diffusion.to(self.device)
            self.vocoder = self.vocoder.to(self.device)
            for b in range(best_results.shape[0]):
                codes = best_results[b].unsqueeze(0)
                latents = best_latents[b].unsqueeze(0)

                # Find the first occurrence of the "calm" token and trim the codes to that.
                ctokens = 0
                for k in range(codes.shape[-1]):
                    if codes[0, k] == calm_token:
                        ctokens += 1
                    else:
                        ctokens = 0
                    if ctokens > 8:  # 8 tokens gives the diffusion model some "breathing room" to terminate speech.
                        latents = latents[:, :k]
                        break

                mel = do_spectrogram_diffusion(self.diffusion, diffuser, latents, diffusion_conditioning,
                                               temperature=diffusion_temperature, verbose=verbose)
                wav = self.vocoder.inference(mel)
                wav_candidates.append(wav.cpu())
            self.diffusion = self.diffusion.cpu()
            self.vocoder = self.vocoder.cpu()

            def potentially_redact(clip, text):
                if self.enable_redaction:
                    return self.aligner.redact(clip.squeeze(1), text).unsqueeze(1)
                return clip

            wav_candidates = [potentially_redact(wav_candidate, text) for wav_candidate in wav_candidates]

            if len(wav_candidates) > 1:
                res = wav_candidates
            else:
                res = wav_candidates[0]

            if return_deterministic_state:
                return res, (deterministic_seed, text, voice_samples, conditioning_latents)
            else:
                return res
            


    def convert_to_audio(self, res):
        # get the audio file from post request

        response = request.post("https://api.puretalk.ai/tts", json={"text": self.text, "voice": self.voice})
        # save audio file
        with open("audio.wav", "wb") as f:
            f.write(response.content)
        # load audio file with librosa
        return librosa.load("audio.wav", sr=22050)

        
        
    def deterministic_state(self, seed=None):
        """
        Sets the random seeds that tortoise uses to the current time() and returns that seed so results can be
        reproduced.
        """
        seed = int(time()) if seed is None else seed
        torch.manual_seed(seed)
        random.seed(seed)
        # Can't currently set this because of CUBLAS. TODO: potentially enable it if necessary.
        # torch.use_deterministic_algorithms(True)

        return seed

# from typing import Dict

# import ray
# from ray import serve
# from starlette.requests import Request



# @serve.deployment(route_prefix="/")
# class Autoregressive:
#     def __init__(self, msg: str):
#         # Initialize model state: could be very large neural net weights.
#         self._msg = msg

#     def __call__(self, request: Request) -> Dict:
#         return {"super": self._msg}


# @serve.deployment(route_prefix="/")
# class Orchestrator:
#     def __init__(self, autoregressive_batch_size=None, models_dir=MODELS_DIR, enable_redaction=True, device=None):
#         # Initialize model state: could be very large neural net weights.
#         self._msg = msg

#     def __call__(self, request: Request) -> Dict:
#         return {"super": self._msg}


# dep = Orchestrator.bind(msg="Hello world!")

from ruth_tts_transformer.parser import TextToSpeech


tts = TextToSpeech("gabby")
tts.tts("Hello world", "gabby_reading")
tts.convert_to_audio()
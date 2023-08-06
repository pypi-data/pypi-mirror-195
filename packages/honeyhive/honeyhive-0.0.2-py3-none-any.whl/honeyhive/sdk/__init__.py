from .datasets import *
from .metrics import *
from .prompts import *
from .tasks import *
from .fine_tuned_models import *
from .generations import *
from .Completions import *
from .feedback import *

import os 
from typing import Optional

api_key = os.environ.get("HONEYHIVE_API_KEY")
# Path of a file with an API key, whose contents can change. Supercedes
# `api_key` if set.  The main use case is volume-mounted Kubernetes secrets,
# which are updated automatically.
api_key_path: Optional[str] = os.environ.get("HONEYHIVE_API_KEY_PATH")

organization = os.environ.get("HONEYHIVE_ORGANIZATION")
api_base = os.environ.get("HONEYHIVE_API_BASE", "https://honeyhive.ai:5000/") #"https://api.honeyhive.ai/v1")

openai_api_key = os.environ.get("OPENAI_API_KEY")
cohere_api_key = os.environ.get("COHERE_API_KEY")
huggingface_api_key = os.environ.get("HUGGINGFACE_API_KEY")

__all__ = [
    "datasets",
    "metrics",
    "prompts",
    "tasks",
    "fine_tuned_models",
    "Completions",
    "generations",
    "feedback",
    "api_key",
    "api_key_path",
    "organization",
    "api_base",
    "openai_api_key",
    "cohere_api_key",
    "huggingface_api_key",
]
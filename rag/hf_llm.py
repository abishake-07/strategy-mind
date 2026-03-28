"""Answer generation via Hugging Face Inference API.

Sends the assembled context prompt to a hosted HF model and returns the generated answer.
"""
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

_DEFAULT_MODEL = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mixtral-8x7B-Instruct-v0.1").strip()
_HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "").strip()


def generate(prompt: str, model: str = None, max_tokens: int = 1024) -> str:
    """Call the HF Inference API with the assembled prompt and return the generated answer."""
    model = (model or _DEFAULT_MODEL).strip()
    client = InferenceClient(model=model, token=_HF_API_KEY)

    response = client.text_generation(
        prompt=prompt,
        max_new_tokens=max_tokens,
        temperature=0.3,
        repetition_penalty=1.1,
        do_sample=True,
    )
    return response.strip()

import os
from typing import Optional
from transformers import pipeline

MODEL_ID = os.getenv("HF_MODEL", "google/gemma-2-2b-it")
HF_TOKEN = os.getenv("HF_TOKEN")

_pipe = None

def get_pipe():
    global _pipe
    if _pipe is None:
        # Basic pipeline (CPU). For production, configure acceleration settings.
        _pipe = pipeline("text-generation", model=MODEL_ID)
    return _pipe

def ask_llm(prompt: str, max_new_tokens: int = 256) -> str:
    pipe = get_pipe()
    out = pipe(prompt, max_new_tokens=max_new_tokens, do_sample=True)
    text = out[0].get("generated_text", "")
    return text

from llm_providers.llm_provider import LLMProvider
from transformers import pipeline
import torch

class LocalProvider(LLMProvider):
    def __init__(self, model_name='meta-llama/Llama-2-7b-chat-hf'):
        self.pipe = pipeline("text-generation",model_name, torch_dtype=torch.bfloat16, device_map="auto")

    def query(self, prompt: str) -> str:
        chat = [
            {"role": "system", "content": "You are a medical expert."},
            {"role": "user", "content": prompt}
        ]
        response = self.pipe(chat, max_new_tokens=512)
        report = response[0]['generated_text'][-1]['content']
        return report

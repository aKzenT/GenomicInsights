from llm_providers.llm_provider import LLMProvider
from transformers import LlamaForCausalLM, LlamaTokenizer
import torch


class LocalProvider(LLMProvider):
    def __init__(self, model_name='meta-llama/Llama-2-7b-hf', device='cpu'):
        self.device = device
        self.tokenizer = LlamaTokenizer.from_pretrained(model_name)
        self.model = LlamaForCausalLM.from_pretrained(model_name).to(self.device)

    def query(self, prompt: str) -> str:
        print(prompt)
        inputs = self.tokenizer(prompt, return_tensors='pt').to(self.device)
        print('tokenized')
        outputs = self.model.generate(**inputs, max_new_tokens=3)
        print('generated')
        report = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        print('decoded')
        return report

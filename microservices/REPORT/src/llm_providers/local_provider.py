import time
from llm_providers.llm_provider import LLMProvider
from transformers import pipeline
import torch

class LocalProvider(LLMProvider):
    def __init__(self, model_name='meta-llama/Llama-2-7b-chat-hf'):
        # Start timing before loading the model
        self.start_time = time.time()
        
        # Load the model
        self.pipe = pipeline("text-generation", model_name, torch_dtype=torch.bfloat16, device_map="auto")
        
        # End timing after the model is loaded
        self.end_time = time.time()

        # Calculate and print the model loading time
        model_loading_time = self.end_time - self.start_time
        print(f"Model loading time: {model_loading_time:.2f} seconds")

    def query(self, prompt: str) -> str:
        chat = [
            {"role": "system", "content": "You are a medical expert."},
            {"role": "user", "content": prompt}
        ]
        
        # Start timing for inference
        start_time = time.time()

        # Generate response
        response = self.pipe(chat, max_new_tokens=512)

        # End timing for inference
        end_time = time.time()

        report = response[0]['generated_text'][-1]['content']

        # Calculate the number of tokens generated
        num_tokens_generated = len(report.split())

        # Calculate the inference time and tokens per second
        inference_time = end_time - start_time
        tokens_per_second = num_tokens_generated / inference_time

        # Output the timing details
        print(f"Inference time: {inference_time:.2f} seconds")
        print(f"Tokens generated: {num_tokens_generated}")
        print(f"Tokens per second: {tokens_per_second:.2f}")
        
        return report

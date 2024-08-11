from abc import ABC, abstractmethod
import os

class LLMProvider(ABC):
    @abstractmethod
    def query(self, prompt: str) -> str:
        pass

def get_provider() -> LLMProvider:
    provider = os.getenv('PROVIDER')
    if provider == 'local':
        from llm_providers.local_provider import LocalProvider
        model = os.getenv('LOCAL_MODEL')
        return LocalProvider(model)
    elif provider == 'openai':
        from llm_providers.openai_provider import OpenAIProvider
        assistant_id = os.getenv('OPENAI_ASSISTANT_ID')
        return OpenAIProvider(assistant_id)
    elif provider == 'hugging_face':
        from llm_providers.hugging_face_provider import HuggingFaceProvider
        username = os.getenv('HUGFACE_USERNAME')
        password = os.getenv('HUGFACE_PASSWORD')
        return HuggingFaceProvider(username, password)
    else:
        raise ValueError(f'Unknown provider: {provider}')
import os
import pytest
from llm_providers.local_provider import LocalProvider
from llm_providers.openai_provider import OpenAIProvider
from llm_providers.hugging_face_provider import HuggingFaceProvider
from dotenv import load_dotenv

load_dotenv()
assistant_id = os.getenv('OPENAI_ASSISTANT_ID')
username = os.getenv('HUGFACE_USERNAME')
password = os.getenv('HUGFACE_PASSWORD')
model = os.getenv('LOCAL_MODEL')
hugchat_model = 'mistralai/Mixtral-8x7B-Instruct-v0.1'

def test_openai_provider():
    provider = OpenAIProvider(assistant_id)
    actual = provider.query('Please respond with hello and nothing else')
    assert actual.strip().lower().startswith('hello')

def test_hugging_face_provider():
    provider = HuggingFaceProvider(username, password, hugchat_model)
    actual = provider.query('Please respond with hello and nothing else')
    assert actual.strip().lower().startswith('hello')

def test_local_provider():
    provider = LocalProvider(model)
    actual = provider.query('Please respond with five random words')
    assert actual.strip().lower().startswith('hello world')

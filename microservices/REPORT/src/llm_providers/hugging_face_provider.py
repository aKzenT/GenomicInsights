from llm_providers.llm_provider import LLMProvider
from hugchat import hugchat
from hugchat.login import Login

class HuggingFaceProvider(LLMProvider):
    def __init__(self, username, password, model: int | str = 0):
        sign = Login(username, password)
        self.cookies = sign.login()
        self.model = model

    def query(self, prompt: str) -> str:
        chatbot = hugchat.ChatBot(cookies=self.cookies.get_dict(), default_llm=self.model)
        query_result = chatbot.chat(prompt, retry_count=5, web_search=False)
        return str(query_result)

from llm_providers.llm_provider import LLMProvider
import openai
import time
import os

class OpenAIProvider(LLMProvider):
    def __init__(self, assistant_id):
        self.client = openai.OpenAI()
        self.assistant = self._create_assistant(assistant_id)

    def _create_assistant(self, assistant_id):
        assistant = self.client.beta.assistants.retrieve(assistant_id)
        return assistant

    def query(self, prompt: str) -> str:
        thread = self.client.beta.threads.create()
        
        self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )

        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant.id,
        )

        run = self._wait_on_run(run, thread)
        messages = self.client.beta.threads.messages.list(thread_id=thread.id, order="asc")
        return self._get_response_from_messages(messages)

    def _wait_on_run(self, run, thread):
        while run.status in ["queued", "in_progress"]:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
        return run

    def _get_response_from_messages(self, messages):
        for message in messages.data:
            if message.role == "assistant":
                return message.content[0].text.value
        return ""
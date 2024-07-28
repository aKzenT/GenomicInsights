import os
import report_helper
from llm_providers.llm_provider import get_provider
from dotenv import load_dotenv

load_dotenv()

def main():
    provider = get_provider()
    result = report_helper.call_LLM(provider, 'Who are you?', 'test', 'test', 'test')
    print(result)

if __name__=="__main__":
    main()
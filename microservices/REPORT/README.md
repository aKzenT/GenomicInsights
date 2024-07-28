To use a Local LLM model you need to authenticate with the Hugging Face API. You can do this by registering at Hugging Face and then running the following command:
```bash
huggingface-cli login
```

For remote Hugging chat API you need to configure the following environment variables:
HUGFACE_USERNAME
HUGFACE_PASSWORD

For OPENAI you need to configure the API key in the OPENAI_API_KEY environment variable.

You can configure these environment variables in a .env file next to this file.
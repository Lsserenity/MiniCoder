from minicoder.llm.openai_client import LLMClient

def main():
    llm = LLMClient()

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Reply with exactly: Hello MiniCoder!"},
    ]

    response = llm.chat(messages)
    print("Model response:")
    print(response.content)

if __name__ == "__main__":
    main()
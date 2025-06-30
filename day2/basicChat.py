from openai import AzureOpenAI
import os
import dotenv

def main():
    client = AzureOpenAI(
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key = os.getenv("AZURE_OPENAI_API_KEY"),
        api_version = "2024-05-01-preview"
    )

    while True:
        print("Please enter your chat or press 'bye' to exit:")
        chat = input("USER: ")
        if chat.lower() == "bye":
            print("Exiting the chat. Goodbye!")
            break
        chat_prompt = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are a chess helper. Answer queries based on chess rules and strategies. For anything else reply I don't know and do not hallucinate"
                    }
                    
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": chat
                    }
                ]
            }
        ]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=chat_prompt            
        )

        print("Response: ", response.choices[0].message.content)
        print("Completion Tokens: ", str(response.usage.completion_tokens))
        print("Prompt Tokens: ", str(response.usage.prompt_tokens))
        print("Total Tokens: ", str(response.usage.total_tokens))

if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
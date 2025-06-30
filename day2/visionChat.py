import base64
import os
import dotenv
from openai import AzureOpenAI

def main():
    client = AzureOpenAI(
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key = os.getenv("AZURE_OPENAI_API_KEY"),
        api_version = "2024-05-01-preview"
    )

    while True:
        print("Please enter your chat or press 'bye' to exit:")
        chat = input("USER: ")

        IMAGE_PATH1 = ""
        IMAGE_PATH2 = ""

        encoded_image1 = base64.b64encode(open(IMAGE_PATH1, "rb").read()).decode("ascii")
        encoded_image2 = base64.b64encode(open(IMAGE_PATH2, "rb").read()).decode("ascii")

        if chat.lower() == "bye":
            print("Exiting the chat. Goodbye!")
            break
        chat_prompt = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an AI assistant that helps people find information."
                    }
                    
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": chat
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image1}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image2}"
                        }
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
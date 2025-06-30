from openai import AzureOpenAI
from PIL import Image
import json
import os
import dotenv
import requests

def main():

    client = AzureOpenAI(
        azure_endpoint=os.getenv("DALLE_ENDPOINT"),
        api_key=os.getenv("DALLE_KEY"),
        api_version="2024-05-01-preview"
    )

    while True:
        print("Please enter your prompt or type 'bye' to exit:")
        chat = input("Prompt: ")
        if chat.lower() == "bye":
            break
        result = client.images.generate(
            model="dall-e-3",
            prompt=chat,
            n=1
        )

        json_response = json.loads(result.model_dump_json())

        image_dir = os.path.join(os.curdir, 'images')

        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        
        image_path = os.path.join(image_dir, 'generated_image.png')

        image_url = json_response['data'][0]['url']
        generated_image = requests.get(image_url).content
        with open(image_path, 'wb') as image_file:
            image_file.write(generated_image)

        image = Image.open(image_path)
        image.show()

if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
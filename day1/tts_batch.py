import requests
import os
import time
import dotenv

def create_batch_synthesis(speech_endpoint, speech_key, synthesis_id, payload):
    url = f"{speech_endpoint}/texttospeech/batchsyntheses/{synthesis_id}?api-version=2024-04-01"
    headers = {
        "Ocp-Apim-Subscription-Key": speech_key,
        "Content-Type": "application/json"
    }
    response = requests.put(url, headers=headers, json=payload)
    response.raise_for_status()
    print(f"Batch synthesis created. Synthesis ID: {synthesis_id}")
    return synthesis_id

def poll_synthesis_status(speech_endpoint, speech_key, synthesis_id):
    status_url = f"{speech_endpoint}/texttospeech/batchsyntheses/{synthesis_id}?api-version=2024-04-01"
    headers = {"Ocp-Apim-Subscription-Key": speech_key}
    while True:
        response = requests.get(status_url, headers=headers)
        response.raise_for_status()
        status = response.json()
        print(f"Status: {status['status']}")
        if status["status"] in ["Succeeded", "Failed"]:
            return status
        time.sleep(5)


def delete_batch_synthesis(speech_endpoint, speech_key, synthesis_id):
    url = f"{speech_endpoint}/texttospeech/batchsyntheses/{synthesis_id}?api-version=2024-04-01"
    headers = {"Ocp-Apim-Subscription-Key": speech_key}
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"Synthesis {synthesis_id} deleted.")
    else:
        print(f"Delete response: {response.status_code} {response.text}")

def download_results(result_url, speech_key, output_file="results.zip"):
    headers = {"Ocp-Apim-Subscription-Key": speech_key}
    response = requests.get(result_url, headers=headers)
    response.raise_for_status()
    with open(output_file, "wb") as f:
        f.write(response.content)
    print(f"Results downloaded to {output_file}")

def main():
    speech_key = "8TUj4KeOFT36haPGFVSvk1fpgj6DWCh9EMqzXRN782YnSVNX587JJQQJ99BFACHYHv6XJ3w3AAAYACOG8fNJ"
    speech_endpoint = "https://eastus2.api.cognitive.microsoft.com/"  # e.g., "https://eastus.api.cognitive.microsoft.com"
    synthesis_id = "123"  # Use a unique string or uuid

    payload = {
        "description": "my ssml test",
        "inputKind": "SSML",
        "inputs": [
            {
                "content": "<speak version=\"1.0\" xml:lang=\"en-US\"><voice name=\"en-US-JennyNeural\">The rainbow has seven colors.</voice></speak>"
            }
        ],
        "properties": {
            "outputFormat": "riff-24khz-16bit-mono-pcm",
            "wordBoundaryEnabled": False,
            "sentenceBoundaryEnabled": False,
            "concatenateResult": False,
            "decompressOutputFiles": False
        }
    }

    # Create batch synthesis
    create_batch_synthesis(speech_endpoint, speech_key, synthesis_id, payload)

    # Poll status until done
    status = poll_synthesis_status(speech_endpoint, speech_key, synthesis_id)
    if status["status"] == "Succeeded":
        print("Synthesis succeeded.")
        # Download results if available
        print(status)        
    else:
        print("Synthesis failed.")

    
    # Optionally delete the batch synthesis
    #delete_batch_synthesis(speech_endpoint, speech_key, synthesis_id)

if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
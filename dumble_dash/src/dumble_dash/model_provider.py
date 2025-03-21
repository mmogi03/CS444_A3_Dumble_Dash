import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def run_model(messages, temperature=0.6, raw=False):
    """
    Calls the Cloudflare API with the given messages and parameters,
    returning the model's response text.
    """
    API_TOKEN = os.getenv("API_TOKEN")
    if not API_TOKEN:
        raise ValueError("API_TOKEN not found in environment. Check your .env file.")

    API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/98847afe353db4215fcd843f27ad1bb8/ai/run/"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    # Specify the model to use – adjust if needed
    model = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
    payload = {
        "messages": messages,
        "temperature": temperature,
        "raw": raw
    }
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=payload)
    result = response.json()
    # Assuming the API returns the output text in result['result']['response']
    return result.get("result", {}).get("response", "")

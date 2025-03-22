import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/98847afe353db4215fcd843f27ad1bb8/ai/run/"
API_TOKEN = os.getenv("CLOUDFLARE_API_KEY")
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def run(model, inputs):
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=inputs)
    print("Status Code:", response.status_code)

    # Check if the response is an image by inspecting the Content-Type header.
    content_type = response.headers.get("Content-Type", "")
    if "image" in content_type:
        # Write the binary image data to output.png.
        with open("output.png", "wb") as f:
            f.write(response.content)
        print("Image saved to output.png")
        return None
    else:
        # If not an image, try to parse JSON.
        try:
            return response.json()
        except Exception as e:
            print("Failed to decode JSON response.")
            print("Response text:", response.text)
            return None


# Set the parameters for image generation.
inputs = {
    "prompt": "wizard",
    "height": 512,
    "width": 512,
    "num_steps": 20,
    "strength": 1,
    "guidance": 7.5
}

output = run("@cf/stabilityai/stable-diffusion-xl-base-1.0", inputs)
if output is not None:
    print(output)

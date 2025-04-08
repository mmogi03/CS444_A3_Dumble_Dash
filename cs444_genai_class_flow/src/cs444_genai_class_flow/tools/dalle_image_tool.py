import os
import uuid
import json
import requests
from pydantic import PrivateAttr
from crewai.tools import BaseTool
from crewai_tools import DallETool

class DownloadingDalleTool(BaseTool):
    name: str = "Downloading DALL·E Tool"
    description: str = (
        "Generates an image using DALL·E and returns the local file path after downloading it."
    )

    # ✅ This lets us attach undeclared attributes like self._dalle
    _dalle: DallETool = PrivateAttr()

    def __init__(self, result_as_answer=True):
        super().__init__(result_as_answer=result_as_answer)
        self._dalle = DallETool(
            model="dall-e-2",
            size="256x256",
            quality="standard",
            n=1
        )

    def _run(self, prompt: str) -> str:
        try:
            print(f"🎨 Generating image with DALL·E for prompt: {prompt}")
            # Use the wrapped DallETool
            image_url = self._dalle(prompt)

            print(f"🌐 Image URL: {image_url}")

            # Download image
            response = requests.get(image_url)
            if response.status_code != 200:
                raise Exception(f"Failed to download image: {response.status_code}")

            os.makedirs("outputs", exist_ok=True)
            filename = f"dalle_image_{uuid.uuid4().hex[:6]}.png"
            path = os.path.join("outputs", filename)

            with open(path, "wb") as f:
                f.write(response.content)

            print(f"✅ Image saved to: {path}")
            return path

        except Exception as e:
            print(f"❌ Error in DownloadingDalleTool: {e}")
            return ""

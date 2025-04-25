import os
import uuid
import json
import requests
import subprocess
from pydantic import PrivateAttr
from crewai.tools import BaseTool
from crewai_tools import DallETool

class DownloadingDalleTool(BaseTool):
    name: str = "Downloading DALL·E Tool"
    description: str = (
        "Generates an image using DALL·E, downloads it, optimizes it using optipng -o7, and returns the local file path."
    )

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
            image_url = self._dalle(prompt)

            print(f"🌐 Image URL: {image_url}")

            response = requests.get(image_url)
            if response.status_code != 200:
                raise Exception(f"Failed to download image: {response.status_code}")

            os.makedirs("outputs", exist_ok=True)
            filename = f"dalle_image_{uuid.uuid4().hex[:6]}.png"
            path = os.path.join("outputs", filename)

            with open(path, "wb") as f:
                f.write(response.content)

            print(f"📦 Image downloaded to: {path}")

            # Run optipng -o7 for lossless compression
            print("🛠 Optimizing image with optipng -o7...")
            subprocess.run(["optipng", "-o7", path], check=True)
            print(f"✅ Image optimized and saved: {path}")

            return path

        except Exception as e:
            print(f"❌ Error in DownloadingDalleTool: {e}")
            return ""

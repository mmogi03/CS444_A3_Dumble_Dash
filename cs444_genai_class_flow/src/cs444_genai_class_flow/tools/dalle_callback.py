import os
import uuid
import requests
import json

def dalle_image_callback(output):
    """
    Callback that downloads the image from the provided image_url in task output,
    saves it as outputs/{name}.png, and returns the saved file path.
    """
    try:
        print(f"🎯 Running callback for task: {output.description}")
        raw = output.raw

        if not isinstance(raw, str):
            print("⚠️ Task output is not a string.")
            return None

        data = json.loads(raw)
        image_url = data.get("image_url")
        name = data.get("name", f"dalle_image_{uuid.uuid4().hex[:6]}")

        if not image_url:
            print("⚠️ No image_url found.")
            return None

        response = requests.get(image_url)
        if response.status_code != 200:
            print(f"❌ Failed to download image: {response.status_code}")
            return None

        os.makedirs("outputs", exist_ok=True)
        filename = f"{name}.png"
        path = os.path.join("outputs", filename)

        with open(path, "wb") as f:
            f.write(response.content)

        print(f"✅ Saved image to {path}")
        return path

    except Exception as e:
        print(f"❌ Callback error: {e}")
        return None


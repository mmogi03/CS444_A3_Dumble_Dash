import os
import uuid
import requests
import json

def dalle_image_callback(output):
    """
    Callback function that downloads and saves DALL·E image if tool output includes image_url.
    Returns the local file path to use as the final task output.
    """
    try:
        print(f"🎯 Running callback for task: {output.description}")

        raw = output.raw

        if not isinstance(raw, str):
            print("⚠️ Task output is not a string. Skipping image download.")
            return None

        data = json.loads(raw)
        image_url = data.get("image_url")

        if not image_url:
            print("⚠️ No 'image_url' found in tool output.")
            return None

        response = requests.get(image_url)
        if response.status_code != 200:
            print(f"❌ Failed to download image from {image_url}")
            return None

        os.makedirs("outputs", exist_ok=True)
        filename = f"dalle_image_{uuid.uuid4().hex[:6]}.png"
        path = os.path.join("outputs", filename)

        with open(path, "wb") as f:
            f.write(response.content)

        print(f"✅ Image saved to {path}")

        # ✅ Return final saved image path
        return path

    except Exception as e:
        print(f"❌ Callback error while downloading image: {e}")
        return None
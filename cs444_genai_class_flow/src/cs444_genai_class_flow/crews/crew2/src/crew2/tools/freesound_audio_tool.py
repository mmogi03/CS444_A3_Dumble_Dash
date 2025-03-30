from crewai.tools import tool
from crew2.tools.sound_search import SoundSearcher
import uuid
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

@tool("FreeSound Audio Generation Tool")
def generate_game_audio(prompt: str) -> str:
    """
    Generates a game audio clip using the FreeSound API based on the provided prompt.
    Returns the path to the generated MP3 file.
    """
    try:
        print("🎧 FreeSound tool called with prompt:", prompt)

        searcher = SoundSearcher()
        filename = f"{prompt[:30].strip().replace(' ', '_')}_{uuid.uuid4().hex[:6]}.mp3"
        output_path = os.path.join("outputs", filename)

        os.makedirs("outputs", exist_ok=True)
        print("🔊 Output path:", output_path)

        searcher.pipeline_self_reflection(prompt, output_path)
        print(f"✅ Audio saved to: {output_path}")

        # ✅ Return only the path string (used in map_assets)
        return output_path

    except Exception as e:
        print(f"❌ Failed to generate audio: {e}")
        return ""

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
        print("FreeSound tool called")
        print("A")
        searcher = SoundSearcher()
        print("B")
        filename = f"{prompt[:30].strip().replace(' ', '_')}_{uuid.uuid4().hex[:6]}.mp3"
        print("C")
        output_path = os.path.join("outputs", filename)
        print("D")

        # Ensure the output directory exists
        os.makedirs("outputs", exist_ok=True)
        print("E")
        
        print("=-=-=-=-= OUTPUT PATH: ", output_path)
        print("=-=-=-=-= PROMPT: ", prompt)

        searcher.pipeline_self_reflection(prompt, output_path)
        print("F")
        return f"✅ Audio generated at: {output_path} for prompt: '{prompt}'"

    except Exception as e:
        print("H")
        return f"❌ Failed to generate audio: {e}"

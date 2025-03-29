from crewai_tools import tool
from sound_search import SoundSearcher
from dotenv import load_dotenv
import os

load_dotenv()  # <-- This reads .env and sets environment variables

@tool("Game Audio Generator")
def generate_game_audio(prompt: str) -> str:
    """Generates game audio based on a prompt using FreeSound and returns the filename."""
    try:
        searcher = SoundSearcher()
        output_filename = "game_audio_output.mp3"
        searcher.pipeline_self_reflection(prompt, output_filename)
        return f"Generated audio and saved to {output_filename}"
    except Exception as e:
        return f"Audio generation failed: {e}"

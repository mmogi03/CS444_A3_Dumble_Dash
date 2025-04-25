from crewai.tools import BaseTool
from .sound_search import SoundSearcher
import uuid
import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class FreeSoundAudioTool(BaseTool):
    name: str = "FreeSound Audio Generation Tool"
    description: str = (
        "Generates a game audio file from a prompt using the FreeSound API and returns the path to the saved .mp3 file."
    )

    def __init__(self, result_as_answer=True):
        super().__init__(result_as_answer=result_as_answer)

    def _run(self, prompt: str) -> str:
        """
        Required by BaseTool. Generates audio and returns file path.
        """
        return self._generate_audio(prompt)

    def __call__(self, prompt: str) -> str:
        """
        This lets it still work like a callable if needed.
        """
        return self._generate_audio(prompt)

    def _generate_audio(self, prompt: str) -> str:
        try:
            print("🎧 FreeSound tool called with prompt:", prompt)

            searcher = SoundSearcher()
            filename_base = f"{prompt[:30].strip().replace(' ', '_')}_{uuid.uuid4().hex[:6]}"
            mp3_path = os.path.join("outputs", f"{filename_base}.mp3")
            ogg_path = os.path.join("outputs", f"{filename_base}.ogg")

            os.makedirs("outputs", exist_ok=True)
            print("🔊 Output path (MP3):", mp3_path)

            # Generate MP3
            searcher.pipeline_self_reflection(prompt, mp3_path)
            print(f"✅ MP3 saved to: {mp3_path}")

            # Convert MP3 to OGG using ffmpeg
            print("🔄 Converting to OGG (quality 4)...")
            subprocess.run([
                "ffmpeg", "-y", "-i", mp3_path,
                "-c:a", "libvorbis", "-qscale:a", "4",
                ogg_path
            ], check=True)
            print(f"✅ OGG saved to: {ogg_path}")

            return mp3_path  # returning original .mp3 path for compatibility

        except Exception as e:
            print(f"❌ Failed to generate audio: {e}")
            return ""

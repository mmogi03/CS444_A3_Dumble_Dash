from crewai.tools import BaseTool
from .sound_search import SoundSearcher
import uuid
import os
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
            filename = f"{prompt[:30].strip().replace(' ', '_')}_{uuid.uuid4().hex[:6]}.mp3"
            output_path = os.path.join("outputs", filename)

            os.makedirs("outputs", exist_ok=True)
            print("🔊 Output path:", output_path)

            searcher.pipeline_self_reflection(prompt, output_path)
            print(f"✅ Audio saved to: {output_path}")

            return output_path

        except Exception as e:
            print(f"❌ Failed to generate audio: {e}")
            return ""

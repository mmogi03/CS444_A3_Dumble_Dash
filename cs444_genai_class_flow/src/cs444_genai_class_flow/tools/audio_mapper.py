from crewai.tools import tool
import json

@tool("integrate_audio_assets")
def integrate_audio_assets(crew2_output: str) -> str:
    """Generates JavaScript code to load and play audio files using crew2_output mapping."""
    try:
        audio_map = json.loads(crew2_output)
    except json.JSONDecodeError:
        return "// Error: Invalid JSON input for audio mapping."

    js_lines = ["// JavaScript Audio Integration"]
    for path, name in audio_map.items():
        short_name = name.replace(" ", "_").lower()
        js_lines.append(f"const {short_name} = new Audio('{path}');")

    js_lines.append("\n// Example usage:")
    js_lines.extend([
        f"{name.replace(' ', '_').lower()}.play();"
        for name in audio_map.values()
    ])

    return "\n".join(js_lines)
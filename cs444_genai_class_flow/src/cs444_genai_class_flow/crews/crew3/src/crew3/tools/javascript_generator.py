# crew3/tools/javascript_generator.py

from crewai.tools import tool
from langchain.llms import OpenAI  # or use OpenAIChat if you're using GPT-4o
import os

@tool("Generate JavaScript code from input prompt")
def generate_javascript_code(prompt: str) -> str:
    """
    Generates JavaScript code based on a textual prompt.
    Useful for generating UI elements, game logic, or scenes for web-based games.
    """

    # Call the OpenAI LLM (or whichever model you're using)
    llm = OpenAI(
        model_name="gpt-4o",  # adjust if needed
        temperature=0.3,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    system_prompt = (
        "You are an expert JavaScript developer. Based on the following instructions, "
        "generate the most clean, idiomatic, and game-oriented JavaScript code possible. "
        "Only output the code, no explanations.\n\n"
    )

    js_code = llm(system_prompt + prompt)
    return js_code

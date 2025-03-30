#!/usr/bin/env python
import warnings
from datetime import datetime

from crews.crew1.crew import Crew1
from crews.crew2.crew import Crew2

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Orchestrate Crew1 and Crew2 in a sequential flow:
    - Crew1 generates the game concept
    - Crew2 creates the story, dialogue, art, and music based on Crew1 output
    """

    print("🚀 Starting Crew1: Game Concept Generation...\n")
    crew1_result = Crew1().crew().kickoff(inputs={
        "topic": "Turn-based roguelike card games",
        "current_year": str(datetime.now().year)
    })

    print("\n✅ Crew1 Completed:")
    print(crew1_result)

    # Extract output from Crew1 to be passed into Crew2
    game_idea = crew1_result.get("generate_unique_game_idea", "")
    if not game_idea:
        print("⚠️ Warning: Crew1 did not return a 'generate_unique_game_idea'. Using placeholder.")
        game_idea = "Placeholder game concept in case Crew1 failed to generate one."

    # Prepare input for Crew2
    crew2_inputs = {
        "generate_unique_game_idea": game_idea,
        "topic": "Turn-based roguelike card games",
        "current_year": str(datetime.now().year)
    }

    print("\n🎮 Starting Crew2: Story, Dialogue, Art, and Audio...\n")
    crew2_result = Crew2().crew().kickoff(inputs=crew2_inputs)

    print("\n✅ Crew2 Completed:")
    print(crew2_result)


# This allows you to run with `crewai run` or `python main.py`
if __name__ == "__main__":
    run()

#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from dumble_dash.crew import DumbleDash

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Kick off the crew to build and refine the Pacman game code.
    """
    inputs = {
        'topic': 'Simple Pacman Game',
        'current_year': str(datetime.now().year)
    }
    try:
        DumbleDash().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {"topic": "Simple Pacman Game"}
    try:
        DumbleDash().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        DumbleDash().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and return the results.
    """
    inputs = {
        "topic": "Simple Pacman Game",
        "current_year": str(datetime.now().year)
    }
    try:
        DumbleDash().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()

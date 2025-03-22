#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from dumble_dash.crew import WizardGame

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Kick off the crew to run the full project and generate an index.html file.
    """
    inputs = {
        'topic': 'Wizard Dungeon Game',
        'current_year': str(datetime.now().year)
    }
    try:
        WizardGame().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {"topic": "Wizard Dungeon Game"}
    try:
        WizardGame().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        WizardGame().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and return the results.
    """
    inputs = {
        "topic": "Wizard Dungeon Game",
        "current_year": str(datetime.now().year)
    }
    try:
        WizardGame().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()

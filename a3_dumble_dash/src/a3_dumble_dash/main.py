#!/usr/bin/env python
import sys
import warnings
from a3_dumble_dash.crew import A3DumbleDash

warnings.filterwarnings("ignore", category=SyntaxWarning)

def run():
    """
    Run the crew.
    """
    inputs = {}  # No extra inputs needed for code generation tasks.
    try:
        A3DumbleDash().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == '__main__':
    run()

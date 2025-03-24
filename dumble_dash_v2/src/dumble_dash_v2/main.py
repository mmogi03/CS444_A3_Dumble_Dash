import sys
import warnings
from datetime import datetime
from dumble_dash_v2.crew import GameProject

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    inputs = {
        'current_year': str(datetime.now().year)
    }
    try:
        GameProject().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(str(e))

def train():
    inputs = {
        'current_year': str(datetime.now().year)
    }
    try:
        GameProject().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(str(e))

def replay():
    try:
        GameProject().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(str(e))

def test():
    inputs = {
        'current_year': str(datetime.now().year)
    }
    try:
        GameProject().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(str(e))

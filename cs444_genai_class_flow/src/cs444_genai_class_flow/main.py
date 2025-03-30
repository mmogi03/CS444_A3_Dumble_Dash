#!/usr/bin/env python
import warnings
from datetime import datetime
import sys
from pathlib import Path
import litellm

# Add the root of the project to the sys.path so imports resolve correctly
sys.path.append(str(Path(__file__).resolve().parent.parent))

from cs444_genai_class_flow.crews.crew1.crew import Crew1
from cs444_genai_class_flow.crews.crew2.crew import Crew2
# from .crews.crew3.src.crew3.crew import Crew3
from crewai.flow import Flow, start, listen
from pydantic import BaseModel

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

class BaseState(BaseModel):
    crew1_output: str = ""
    crew2_output: str = ""
    crew3_output: str = ""

class CrewsFlow(Flow[BaseState]):
    def __init__(self):
        super().__init__()
        print("CrewsFlow initialized")

    @start()
    def run_crew1(self):
        print("Running crew 1")
        crew1 = Crew1().crew()

        # Debug: show which tasks are loaded
        print("Tasks loaded into Crew1:")
        for task in crew1.tasks:
            print(f"- {task.description}")

        # Run the crew
        result = crew1.kickoff()

        # Debug: raw result and type
        print("Crew 1 raw result:", result)
        print("Crew 1 result type:", type(result))

        # Handle various possible result formats
        if result:
            if isinstance(result, list):
                print("Result is a list of task outputs:")
                for i, r in enumerate(result):
                    print(f"  Task {i+1} output:", r)
                self.state.crew1_output = "\n".join(map(str, result))

            elif isinstance(result, dict):
                print("Result is a dict of task outputs:")
                for k, v in result.items():
                    print(f"  {k}: {v}")
                self.state.crew1_output = "\n".join(f"{k}: {v}" for k, v in result.items())

            else:
                print("Result is a single object:", result)
                self.state.crew1_output = str(result)
        else:
            print("Crew 1 returned nothing")


    @listen(run_crew1)
    def run_crew2(self):
        print("Running crew 2")
        crew2 = Crew2().crew()
        result = crew2.kickoff(inputs = {"crew1_output": self.state.crew1_output})
        print("Crew 2 raw result:", result)
        print("Crew 2 result type:", type(result))

        if result:
            if isinstance(result, list):
                self.state.crew2_output = "\n".join(map(str, result))
            elif isinstance(result, dict):
                self.state.crew2_output = "\n".join(f"{k}: {v}" for k, v in result.items())
            else:
                self.state.crew2_output = str(result)
        else:
            print("Crew 2 returned nothing")

    # @listen(run_crew2)
    # def run_crew3(self):
    #     print("Running crew 3")
    #     result = (
    #         Crew3().crew().kickoff()
    #     )
    #     print("Crew 3 done", result.raw)
    #     self.state.crew3_output = result.raw   

def kickoff():
    print("Starting kickoff()")
    crews_flow = CrewsFlow()
    crews_flow.kickoff()
    print("Crew1 output:", crews_flow.state.crew1_output)
    print("Crew2 output:", crews_flow.state.crew2_output)

def plot():
    crews_flow = CrewsFlow()
    crews_flow.plot()

if __name__ == "__main__":
    kickoff()
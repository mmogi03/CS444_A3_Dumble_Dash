import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.llm import LLM

# Instantiate the desired LLM instance
llm = LLM(
    model="cloudflare/@cf/meta/llama-3.3-70b-instruct-fp8-fast",
    base_url="https://api.cloudflare.com/client/v4/accounts/98847afe353db4215fcd843f27ad1bb8/ai/run/",
    api_key=os.getenv("CLOUDFLARE_API_KEY"),
    max_tokens=13000
)

@CrewBase
class A3DumbleDash():
    """A3DumbleDash crew for file-specific code generation"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def boot_scene_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['boot_scene_agent'],
            llm=llm,
            verbose=True,
            max_execution_time=None
        )

    @agent
    def overworld_scene_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['overworld_scene_agent'],
            llm=llm,
            verbose=True,
            max_execution_time=None
        )

    @agent
    def audio_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['audio_agent'],
            llm=llm,
            verbose=True,
            max_execution_time=None
        )

    @agent
    def battle_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['battle_agent'],
            llm=llm,
            verbose=True,
            max_execution_time=None
        )

    @agent
    def maze_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['maze_agent'],
            llm=llm,
            verbose=True,
            max_execution_time=None
        )

    @agent
    def ui_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['ui_agent'],
            llm=llm,
            verbose=True,
            max_execution_time=None
        )

    @agent
    def main_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['main_agent'],
            llm=llm,
            verbose=True,
            max_execution_time=None
        )

    @agent
    def index_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['index_agent'],
            llm=llm,
            verbose=True,
            max_execution_time=None
        )

    @task
    def boot_scene_task(self) -> Task:
        return Task(
            config=self.tasks_config['boot_scene_task'],
            output_file='output/src/scenes/BootScene.js'
        )

    @task
    def overworld_scene_task(self) -> Task:
        return Task(
            config=self.tasks_config['overworld_scene_task'],
            output_file='output/src/scenes/OverworldScene.js'
        )

    @task
    def audio_task(self) -> Task:
        return Task(
            config=self.tasks_config['audio_task'],
            output_file='output/src/utils/audio.js'
        )

    @task
    def battle_task(self) -> Task:
        return Task(
            config=self.tasks_config['battle_task'],
            output_file='output/src/utils/battle.js'
        )

    @task
    def maze_task(self) -> Task:
        return Task(
            config=self.tasks_config['maze_task'],
            output_file='output/src/utils/maze.js'
        )

    @task
    def ui_task(self) -> Task:
        return Task(
            config=self.tasks_config['ui_task'],
            output_file='output/src/utils/ui.js'
        )

    @task
    def main_task(self) -> Task:
        return Task(
            config=self.tasks_config['main_task'],
            output_file='output/main.js'
        )

    @task
    def index_task(self) -> Task:
        return Task(
            config=self.tasks_config['index_task'],
            output_file='output/index.html'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

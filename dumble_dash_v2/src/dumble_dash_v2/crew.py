from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import DallETool

@CrewBase
class GameProject:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def manager(self):
        return Agent(config=self.agents_config['manager'])

    @agent
    def game_logic_generation(self):
        return Agent(config=self.agents_config['game_logic_generation'])

    @agent
    def theme_generation(self):
        return Agent(config=self.agents_config['theme_generation'])

    @agent
    def ui_ux(self):
        # Include DallETool so the UI/UX agent can generate images.
        return Agent(
            config=self.agents_config['ui_ux'],
            tools=[DallETool(model="dall-e-3", size="256x256", quality="standard", n=1)]
        )

    @agent
    def user_input(self):
        return Agent(config=self.agents_config['user_input'])

    @agent
    def code_integration(self):
        return Agent(config=self.agents_config['code_integration'])

    @agent
    def test_debug(self):
        return Agent(config=self.agents_config['test_debug'])

    @task
    def theme_task(self):
        return Task(config=self.tasks_config['theme_task'])

    @task
    def game_logic_task(self):
        return Task(config=self.tasks_config['game_logic_task'])

    @task
    def user_input_task(self):
        return Task(config=self.tasks_config['user_input_task'])

    @task
    def code_integration_task(self):
        return Task(config=self.tasks_config['code_integration_task'])

    @task
    def ui_ux_task(self):
        return Task(config=self.tasks_config['ui_ux_task'])

    @task
    def testing_debug_task(self):
        return Task(config=self.tasks_config['testing_debug_task'])

    @task
    def manager_task(self):
        return Task(config=self.tasks_config['manager_task'])

    @crew
    def crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

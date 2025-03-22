from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class DumbleDashV2():
    """DumbleDashV2 crew for HTML5 Phaser.js game generated entirely by agents into an output folder"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def html_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['html_generator'],
            verbose=True
        )

    @agent
    def game_logic_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['game_logic_generator'],
            verbose=True
        )

    @agent
    def enemy_logic_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['enemy_logic_generator'],
            verbose=True
        )

    @agent
    def ui_and_assets_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['ui_and_assets_manager'],
            verbose=True
        )

    @agent
    def debug_and_review_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['debug_and_review_agent'],
            verbose=True
        )

    @task
    def generate_html(self) -> Task:
        return Task(
            config=self.tasks_config['generate_html'],
            output_file='output/index.html'
        )

    @task
    def generate_game_logic(self) -> Task:
        return Task(
            config=self.tasks_config['generate_game_logic'],
            output_file='output/js/game.js'
        )
        
    @task
    def generate_enemy_logic(self) -> Task:
        return Task(
            config=self.tasks_config['generate_enemy_logic'],
            output_file='output/js/game_enemies.js'
        )

    @task
    def integrate_ui_assets(self) -> Task:
        return Task(
            config=self.tasks_config['integrate_ui_assets']
        )

    @task
    def debug_and_review(self) -> Task:
        return Task(
            config=self.tasks_config['debug_and_review'],
            output_file='debug_report.txt'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # Automatically created by @agent decorators.
            tasks=self.tasks,    # Automatically created by @task decorators.
            process=Process.sequential,
            verbose=True,
            planning=True
            # memory=True
        )

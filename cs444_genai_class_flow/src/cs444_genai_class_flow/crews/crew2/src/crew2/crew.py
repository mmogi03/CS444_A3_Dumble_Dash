from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, crew, task
from crew2.tools.freesound_audio_tool import generate_game_audio


@CrewBase
class Crew2():
    """Crew2: Story, Dialogue, and Audio based on Crew1 output"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # === LLM ===
    llm = LLM(model="openai/gpt-4o", temperature=0)

    # === AGENTS ===

    @agent
    def main_menu_composer(self) -> Agent:
        return Agent(
            config=self.agents_config['main_menu_composer'],
            tools=[generate_game_audio],
            verbose=True,
            llm=self.llm
        )

    @agent
    def background_loop_composer(self) -> Agent:
        return Agent(
            config=self.agents_config['background_loop_composer'],
            tools=[generate_game_audio],
            verbose=True,
            llm=self.llm
        )

    @agent
    def victory_theme_composer(self) -> Agent:
        return Agent(
            config=self.agents_config['victory_theme_composer'],
            tools=[generate_game_audio],
            verbose=True,
            llm=self.llm
        )

    @agent
    def defeat_theme_composer(self) -> Agent:
        return Agent(
            config=self.agents_config['defeat_theme_composer'],
            tools=[generate_game_audio],
            verbose=True,
            llm=self.llm
        )

    @agent
    def story_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['story_designer'],
            verbose=True
        )

    @agent
    def dialogue_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['dialogue_writer'],
            verbose=True
        )

    # === TASKS ===

    @task
    def design_story(self) -> Task:
        return Task(
            config=self.tasks_config['design_story'],
            agent=self.story_designer()
        )

    @task
    def write_dialogue(self) -> Task:
        return Task(
            config=self.tasks_config['write_dialogue'],
            agent=self.dialogue_writer()
        )

    @task
    def generate_main_menu_music(self) -> Task:
        return Task(
            config=self.tasks_config['generate_main_menu_music'],
            agent=self.main_menu_composer()
        )

    @task
    def generate_background_loop(self) -> Task:
        return Task(
            config=self.tasks_config['generate_background_loop'],
            agent=self.background_loop_composer()
        )

    @task
    def generate_victory_music(self) -> Task:
        return Task(
            config=self.tasks_config['generate_victory_music'],
            agent=self.victory_theme_composer()
        )

    @task
    def generate_defeat_music(self) -> Task:
        return Task(
            config=self.tasks_config['generate_defeat_music'],
            agent=self.defeat_theme_composer()
        )

    # === CREW ===

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

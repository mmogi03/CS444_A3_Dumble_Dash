from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Crew1():
    """Crew1 crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def find_game_concept(self) -> Agent:
        return Agent(
            config=self.agents_config['find_game_concept_a'],
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def scrap_game_concept(self) -> Agent:
        return Agent(
            config=self.agents_config['scrap_game_concept_a'],
            tools=[ScrapeWebsiteTool()],
            verbose=True
        )

    @agent
    def create_innovative_game_concept(self) -> Agent:
        return Agent(
            config=self.agents_config['create_innovative_game_concept_a'],
            verbose=True,
            memory=True
        )


    @task
    def search_trending_concepts(self) -> Task:
        return Task(
            config=self.tasks_config['search_trending_concepts_a'],
            agent=self.find_game_concept()
        )

    @task
    def scrape_card_battler_ideas(self) -> Task:
        return Task(
            config=self.tasks_config['scrape_card_battler_ideas_a'],
            agent=self.scrap_game_concept()
        )

    @task
    def generate_unique_game_idea(self) -> Task:
        return Task(
            config=self.tasks_config['generate_unique_game_idea_a'],
            agent=self.create_innovative_game_concept()

        )

    @crew
    def crew(self) -> Crew:
        """Creates the Cs444GenaiClass crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

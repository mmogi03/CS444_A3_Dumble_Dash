from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileWriterTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators



@CrewBase
class Cs444GenaiClass():
    """Cs444GenaiClass crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def visual_concept_agent(self) -> Agent:
        return Agent(
            config = self.agents_config['visual_concept_agent'], 
            verbose = True, 
            memory = True,  # I think this still needs memory, no ? - vv 
        )
    
    @agent
    def audio_director(self) -> Agent:
        return Agent(
            config = self.agents_config['audio_director'], 
            verbose = True, 
            memory = True,  # I think this still needs memory, no ? - vv 
        )

    @agent
    def story_designer(self) -> Agent:
        return Agent(
            config = self.agents_config['story_designer'], 
            verbose = True, 
            memory = True, # I think this still needs memory, no ? - vv 
        )

    @agent 
    def dialogue_writer(self) -> Agent:
        return Agent(
            config = self.agents_config['dialogue_writer'], 
            verbose = True, 
            memory = True, # I think this still needs memory, no ? - vv 
        )
    
    # @task
    # def design_story(self) -> Task:
    #     return Task(
    #         config = self.tasks_config['design_story'],
    #         agent = self.story_designer()
    #     )

    # @task 
    # def write_dialogue(self) -> Task:
    #     return Task(
    #         config = self.tasks_config['write_dialogue'],
    #         agent = self.dialogue_writer()
    #     )

    # @task 
    # def make_art(self) -> Task: 
    #     return Task(
    #         config = self.tasks_config['make_art'],
    #         agent = self.visual_concept_agent()
    #     )
    
    # @task 
    # def make_music(self) -> Task: 
    #     return Task(
    #         config = self.tasks_config['make_music'],
    #         agent = self.audio_director()
    #     )


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
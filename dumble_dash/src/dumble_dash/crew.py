import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

# Create the general LLM instance.
llm = LLM(
    model="cloudflare/@cf/meta/llama-3.3-70b-instruct-fp8-fast",
    base_url="https://api.cloudflare.com/client/v4/accounts/98847afe353db4215fcd843f27ad1bb8/ai/run/",
    api_key=os.getenv("CLOUDFLARE_API_KEY"),
    max_tokens=2048
)

@CrewBase
class WizardGame():
    # Paths to the configuration files (relative to the project root).
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # --- Agent Definitions ---
    @agent
    def player_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['player_agent'],
            llm=llm,
            verbose=True
        )

    @agent
    def enemy_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['enemy_agent'],
            llm=llm,
            verbose=True
        )

    @agent
    def boss_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['boss_agent'],
            llm=llm,
            verbose=True
        )

    @agent
    def map_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['map_agent'],
            llm=llm,
            verbose=True
        )

    @agent
    def interactions_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['interactions_agent'],
            llm=llm,
            verbose=True
        )

    @agent
    def spells_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['spells_agent'],
            llm=llm,
            verbose=True
        )

    @agent
    def template_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['template_agent'],
            llm=llm,
            verbose=True
        )

    @agent
    def debugger_code_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['debugger_code_reviewer'],
            llm=llm,
            verbose=True
        )

    @agent
    def input_controls_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['input_controls_agent'],
            llm=llm,
            verbose=True
        )

    @agent
    def project_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['project_manager'],
            llm=llm,
            verbose=True
        )

    # --- Task Definitions ---
    @task
    def player_system_task(self) -> Task:
        return Task(config=self.tasks_config['player_system_task'])

    @task
    def enemy_system_task(self) -> Task:
        return Task(config=self.tasks_config['enemy_system_task'])

    @task
    def boss_system_task(self) -> Task:
        return Task(config=self.tasks_config['boss_system_task'])

    @task
    def map_generation_task(self) -> Task:
        return Task(config=self.tasks_config['map_generation_task'])

    @task
    def interaction_system_task(self) -> Task:
        return Task(config=self.tasks_config['interaction_system_task'])

    @task
    def spell_system_task(self) -> Task:
        return Task(config=self.tasks_config['spell_system_task'])

    @task
    def template_menu_task(self) -> Task:
        return Task(config=self.tasks_config['template_menu_task'])

    @task
    def debugging_review_task(self) -> Task:
        return Task(config=self.tasks_config['debugging_review_task'])

    @task
    def controls_integration_task(self) -> Task:
        return Task(config=self.tasks_config['controls_integration_task'])

    @task
    def basic_art_task(self) -> Task:
        return Task(config=self.tasks_config['basic_art_task'])

    @task
    def integration_task(self) -> Task:
        return Task(
            config=self.tasks_config['integration_task'],
            output_file="index.html"
        )

    # --- Crew Assembly ---
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

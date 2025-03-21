import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

# Create the LLM instance.
# Make sure your CLOUDFLARE_API_KEY environment variable is set.
llm = LLM(
    model="cloudflare/@cf/meta/llama-3.3-70b-instruct-fp8-fast",
    base_url="https://api.cloudflare.com/client/v4/accounts/98847afe353db4215fcd843f27ad1bb8/ai/run/",
    api_key=os.getenv("CLOUDFLARE_API_KEY"),
    max_tokens=2048  # Increase the max tokens for longer output
)

@CrewBase
class DumbleDash():
    # Provide the paths to your configuration files (relative to the project root).
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def game_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['game_developer'],
            llm=llm,
            verbose=True
        )

    @agent
    def code_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['code_reviewer'],
            llm=llm,
            verbose=True
        )

    @task
    def development_task(self) -> Task:
        return Task(
            config=self.tasks_config['development_task'],
        )

    @task
    def review_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_task'],
            output_file='pacman_game.html'  # Final output code saved here.
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

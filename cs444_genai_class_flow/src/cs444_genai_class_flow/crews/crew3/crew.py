import os
from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, crew, task
from ...tools.audio_mapper import integrate_audio_assets

# Make Javascipt Agent
# Pass template.html into the project manager agent through tasks
# Maybe find a way to test the HTML and the CSS somehow 
# Debugging agent ensures no errors in the code

@CrewBase
class Crew3():
    """Crew3: Converts story and audio into full JavaScript game code"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    llm = LLM(model="openai/gpt-4o", temperature=0)

    # === AGENTS ===

    @agent
    def project_manager(self) -> Agent:
        return Agent(config=self.agents_config['project_manager'], 
                     verbose=True, llm=self.llm,
                     allow_code_execution = True, 
                     language = "JavaScript")

    @agent
    def ui_developer(self) -> Agent:
        return Agent(config=self.agents_config['ui_developer'], 
                     verbose=True, llm=self.llm)

    @agent
    def gameplay_logic_developer(self) -> Agent:
        return Agent(config=self.agents_config['gameplay_logic_developer'], 
                     verbose=True, llm=self.llm)

    @agent
    def audio_integrator(self) -> Agent:
        return Agent(config=self.agents_config['audio_integrator'], 
                     tools=[integrate_audio_assets], verbose=True, 
                     llm=self.llm)

    @agent
    def scene_builder(self) -> Agent:
        return Agent(config=self.agents_config['scene_builder'], 
                     verbose=True, llm=self.llm)

    @agent
    def game_exporter(self) -> Agent:
        return Agent(config=self.agents_config['game_exporter'], 
                     verbose=True, llm=self.llm)

    @agent
    def html_css_specialist(self) -> Agent:
        return Agent(config=self.agents_config['html_css_specialist'], 
                     verbose=True, llm=self.llm)

    @agent
    def build_system_engineer(self) -> Agent:
        return Agent(config=self.agents_config['build_system_engineer'], 
                     verbose=True, llm=self.llm)
    
    @agent 
    def js_debugger(self) -> Agent:
        return Agent(config = self.agents_config['js_debugger'], 
                     verboes = True, llm = self.llm, allow_code_execution = True, 
                     language = "JavaScript")
    
    @agent
    def html_debugger(self) -> Agent:
        return Agent(config = self.agents_config['html_debugger'], 
                     verboes = True, llm = self.llm)
    
    @agent
    def css_debugger(self) -> Agent:
        return Agent(config = self.agents_config['css_debugger'], 
                     verboes = True, llm = self.llm)
    
    @agent
    def qc_engineer(self) -> Agent:
        return Agent(config = self.agents_config['qc_engineer'], 
                     verboes = True, llm = self.llm)

    # === TASKS ===

    @task
    def build_ui(self) -> Task:
        return Task(config=self.tasks_config['build_ui'], 
                    agent=self.ui_developer(), 
                    output_file="output/ui.js")
    
    @task
    def dg_build_ui(self) -> Task:
        return Task(config=self.tasks_config['dg_build_ui'], 
                    agent=self.js_debugger(), 
                    output_file="output/ui.js")

    @task
    def develop_gameplay_logic(self) -> Task:
        return Task(config=self.tasks_config['develop_gameplay_logic'], 
                    agent=self.gameplay_logic_developer(), 
                    output_file="output/gameplay_logic.js")
    
    @task
    def dg_develop_gameplay_logic(self) -> Task:
        return Task(config=self.tasks_config['dg_develop_gameplay_logic'], 
                    agent=self.js_debugger(), 
                    output_file="output/gameplay_logic.js")

    @task
    def add_audio(self) -> Task:
        return Task(config=self.tasks_config['add_audio'], 
                    agent=self.audio_integrator(), 
                    output_file="output/audio.js")
    
    @task
    def dg_add_audio(self) -> Task:
        return Task(config=self.tasks_config['dg_add_audio'], 
                    agent=self.js_debugger(), 
                    output_file="output/audio.js")

    @task
    def construct_scenes(self) -> Task:
        return Task(config=self.tasks_config['construct_scenes'], 
                    agent=self.scene_builder(), 
                    output_file="output/scenes.js")
    
    @task
    def dg_construct_scenes(self) -> Task:
        return Task(config=self.tasks_config['dg_construct_scenes'], 
                    agent=self.scene_builder(), 
                    output_file="output/scenes.js")

    @task
    def generate_index_html(self) -> Task:
        return Task(config=self.tasks_config['generate_index_html'], 
                    agent=self.html_css_specialist(), 
                    output_file="output/index.html")
    
    @task
    def dg_generate_index_html(self) -> Task:
        return Task(
            config = self.tasks_config['dg_generate_index_html'],
            agent = self.html_debugger(),
            output_file = "output/index.html"
        )

    @task
    def generate_style_css(self) -> Task:
        return Task(config=self.tasks_config['generate_style_css'], 
                    agent=self.html_css_specialist(), 
                    output_file="output/style.css")
    
    @task
    def dg_generate_style_css(self) -> Task:
        return Task(config=self.tasks_config['dg_generate_style_css'], 
                    agent=self.css_debugger(), 
                    output_file="output/style.css")

    @task
    def generate_game_entry_point(self) -> Task:
        return Task(config=self.tasks_config['generate_game_entry_point'], 
                    agent=self.build_system_engineer(), 
                    output_file="output/main.js")
    
    @task
    def dg_generate_game_entry_point(self) -> Task:
        return Task(config=self.tasks_config['dg_generate_game_entry_point'], 
                    agent=self.js_debugger(), 
                    output_file="output/main.js")

    @task
    def bundle_and_export_game(self) -> Task:
        return Task(config=self.tasks_config['bundle_and_export_game'],
                    agent=self.build_system_engineer(), 
                    output_file="output/BUILD_INSTRUCTIONS.txt")

    @task
    def export_game_code(self) -> Task:
        return Task(config=self.tasks_config['export_game_code'], 
                    agent=self.game_exporter(), 
                    output_file="output/final_bundle.js")
    
    @task
    def check_integrated_code(self) -> Task:
        return Task(config = self.tasks_config['check_integrated_code'],
                    agent = self.qc_engineer())

    # === CREW ===

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.ui_developer(),
                self.gameplay_logic_developer(),
                self.audio_integrator(),
                self.scene_builder(),
                self.game_exporter(),
                self.html_css_specialist(),
                self.build_system_engineer(), 
                self.js_debugger(),
                self.html_debugger(),
                self.css_debugger()
            ],
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=self.project_manager(),
            verbose=True
        )
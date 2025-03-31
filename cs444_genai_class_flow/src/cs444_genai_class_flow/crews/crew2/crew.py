from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, crew, task
#from crew2.tools.freesound_audio_tool import generate_game_audio
from ...tools.freesound_audio_tool import FreeSoundAudioTool

from ...tools.dalle_callback import dalle_image_callback
from crewai_tools import DallETool
from pydantic import BaseModel
from typing import List

# === JSON Output Model for map_assets ===
class AssetMap(BaseModel):
    main_character_icon: str
    enemy_icons: List[str]
    environment_background: str
    card_image: str
    menu_music: str
    background_music: str
    victory_music: str
    defeat_music: str
    game_icon: str
    floor_texture: str

@CrewBase
class Crew2():
    """Crew2: Story, Dialogue, and Audio based on Crew1 output"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # === LLMs and Tools ===
    llm = LLM(model="openai/gpt-4o", temperature=0)
    dalle_tool = DallETool(model="dall-e-2",
                        size="256x256",
                        quality="standard",
                        n=1)

    # === AGENTS ===
    
    @agent
    def visual_concept_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['visual_concept_agent'],
            tools=[self.dalle_tool],
            verbose=True,
            llm=self.llm,
            memory=True
        )

    @agent
    def main_menu_composer(self) -> Agent:
        return Agent(
            config=self.agents_config['main_menu_composer'],
            tools=[FreeSoundAudioTool(result_as_answer=True)],
            verbose=True,
            llm=self.llm,
            memory=True
        )

    @agent
    def background_loop_composer(self) -> Agent:
        return Agent(
            config=self.agents_config['background_loop_composer'],
            tools=[FreeSoundAudioTool(result_as_answer=True)],
            verbose=True,
            llm=self.llm,
            memory=True
        )

    @agent
    def victory_theme_composer(self) -> Agent:
        return Agent(
            config=self.agents_config['victory_theme_composer'],
            tools=[FreeSoundAudioTool(result_as_answer=True)],
            verbose=True,
            llm=self.llm,
            memory=True
        )

    @agent
    def defeat_theme_composer(self) -> Agent:
        return Agent(
            config=self.agents_config['defeat_theme_composer'],
            tools=[FreeSoundAudioTool(result_as_answer=True)],
            verbose=True,
            llm=self.llm,
            memory=True
        )

    @agent
    def story_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['story_designer'],
            verbose=True,
            memory=True
        )

    @agent
    def dialogue_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['dialogue_writer'],
            verbose=True,
            memory=True
        )
        
    @agent
    def asset_mapper(self) -> Agent:
        return Agent(
            config=self.agents_config['asset_mapper'],
            verbose=True,
            llm=self.llm,
            memory=True
        )

    # === TASKS ===

    @task
    def design_story(self) -> Task:
        return Task(
            config=self.tasks_config['design_story'],
            agent=self.story_designer(),
            # async_execution=False
        )

    @task
    def write_dialogue(self) -> Task:
        return Task(
            config=self.tasks_config['write_dialogue'],
            agent=self.dialogue_writer(),
            # async_execution=False
        )

    @task
    def generate_main_menu_music(self) -> Task:
        return Task(
            config=self.tasks_config['generate_main_menu_music'],
            agent=self.main_menu_composer(),
            # async_execution=True
        )

    @task
    def generate_background_loop(self) -> Task:
        return Task(
            config=self.tasks_config['generate_background_loop'],
            agent=self.background_loop_composer(),
            # async_execution=True
        )

    @task
    def generate_victory_music(self) -> Task:
        return Task(
            config=self.tasks_config['generate_victory_music'],
            agent=self.victory_theme_composer(),
            # async_execution=True
        )

    @task
    def generate_defeat_music(self) -> Task:
        return Task(
            config=self.tasks_config['generate_defeat_music'],
            agent=self.defeat_theme_composer(),
            # async_execution=True
        )

    @task
    def generate_main_character_icon(self) -> Task:
        return Task(
            config=self.tasks_config['generate_main_character_icon'],
            agent=self.visual_concept_agent(),
            callback=dalle_image_callback,
            # async_execution=True
        )

    @task
    def generate_enemy_icons(self) -> Task:
        return Task(
            config=self.tasks_config['generate_enemy_icons'],
            agent=self.visual_concept_agent(),
            callback=dalle_image_callback,
            # async_execution=True
        )

    @task
    def generate_environment_visuals(self) -> Task:
        return Task(
            config=self.tasks_config['generate_environment_visuals'],
            agent=self.visual_concept_agent(),
            callback=dalle_image_callback,
            # async_execution=True
        )

    @task
    def generate_game_icon(self) -> Task:
        return Task(
            config=self.tasks_config['generate_game_icon'],
            agent=self.visual_concept_agent(),
            callback=dalle_image_callback,
            # async_execution=True
        )
        
    @task
    def generate_card_image(self) -> Task:
        return Task(
            config=self.tasks_config['generate_card_image'],
            agent=self.visual_concept_agent(),
            callback=dalle_image_callback,
            # async_execution=True
        )
        
    @task
    def generate_floor_texture(self) -> Task:
        return Task(
            config=self.tasks_config['generate_floor_texture'],
            agent=self.visual_concept_agent(),
            callback=dalle_image_callback,
            # async_execution=True
        )

    @task
    def map_assets(self) -> Task:
        return Task(
            config=self.tasks_config['map_assets'],
            agent=self.asset_mapper(),
            output_json=AssetMap,
            # async_execution=False
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

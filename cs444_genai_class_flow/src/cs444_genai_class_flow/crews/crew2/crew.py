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
    card_attack_sound_1: str
    card_attack_sound_2: str
    heal_sound: str
    enemy_attack_sound: str
    background_music: str
    endgame_music: str
    level_victory_sound: str
    start_game_sound: str
    game_icon: str
    floor_texture: str
    boss_music: str
    boss_icon: str

@CrewBase
class Crew2():
    """Crew2: Story and Audio based on Crew1 output"""

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
    def boss_visual_artist(self) -> Agent:
        return Agent(
            config=self.agents_config['boss_visual_artist'],
            tools=[self.dalle_tool],
            verbose=True,
            llm=self.llm,
            memory=True
        )

    @agent
    def main_character_card_sound_composer(self) -> Agent:
        return Agent(
            config=self.agents_config['main_character_card_sound_composer'],
            tools=[FreeSoundAudioTool(result_as_answer=True)],
            verbose=True,
            llm=self.llm,
            memory=True
        )

    @agent
    def enemy_sound_composer(self) -> Agent:
        return Agent(
            config=self.agents_config['enemy_sound_composer'],
            tools=[FreeSoundAudioTool(result_as_answer=True)],
            verbose=True,
            llm=self.llm,
            memory=True
        )
        
    @agent
    def boss_music_composer(self) -> Agent:
        return Agent(
            config=self.agents_config['boss_music_composer'],
            tools=[FreeSoundAudioTool(result_as_answer=True)],
            verbose=True,
            llm=self.llm,
            memory=True
        )

    @agent
    def background_music_composer(self) -> Agent:
        return Agent(
            config=self.agents_config['background_music_composer'],
            tools=[FreeSoundAudioTool(result_as_answer=True)],
            verbose=True,
            llm=self.llm,
            memory=True
        )

    @agent
    def endgame_music_composer(self) -> Agent:
        return Agent(
            config=self.agents_config['endgame_music_composer'],
            tools=[FreeSoundAudioTool(result_as_answer=True)],
            verbose=True,
            llm=self.llm,
            memory=True
        )

    @agent
    def victory_sound_composer(self) -> Agent:
        return Agent(
            config=self.agents_config['victory_sound_composer'],
            tools=[FreeSoundAudioTool(result_as_answer=True)],
            verbose=True,
            llm=self.llm,
            memory=True
        )

    @agent
    def start_game_sound_composer(self) -> Agent:
        return Agent(
            config=self.agents_config['start_game_sound_composer'],
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
    def generate_card_attack_sound_1(self) -> Task:
        return Task(
            config=self.tasks_config['generate_card_attack_sound_1'],
            agent=self.main_character_card_sound_composer(),
        )

    @task
    def generate_card_attack_sound_2(self) -> Task:
        return Task(
            config=self.tasks_config['generate_card_attack_sound_2'],
            agent=self.main_character_card_sound_composer(),
        )

    @task
    def generate_heal_sound(self) -> Task:
        return Task(
            config=self.tasks_config['generate_heal_sound'],
            agent=self.main_character_card_sound_composer(),
        )

    @task
    def generate_enemy_attack(self) -> Task:
        return Task(
            config=self.tasks_config['generate_enemy_attack'],
            agent=self.enemy_sound_composer(),
        )

    @task
    def generate_background_music(self) -> Task:
        return Task(
            config=self.tasks_config['generate_background_music'],
            agent=self.background_music_composer(),
        )

    @task
    def generate_endgame_music(self) -> Task:
        return Task(
            config=self.tasks_config['generate_endgame_music'],
            agent=self.endgame_music_composer(),
        )

    @task
    def generate_level_victory(self) -> Task:
        return Task(
            config=self.tasks_config['generate_level_victory'],
            agent=self.victory_sound_composer(),
        )

    @task
    def generate_start_game_sound(self) -> Task:
        return Task(
            config=self.tasks_config['generate_start_game_sound'],
            agent=self.start_game_sound_composer(),
        )
        
    @task
    def generate_boss_music(self) -> Task:
        return Task(
            config=self.tasks_config['generate_boss_music'],
            agent=self.boss_music_composer(),
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
    def generate_boss_icon(self) -> Task:
        return Task(
            config=self.tasks_config['generate_boss_icon'],
            agent=self.boss_visual_artist(),
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
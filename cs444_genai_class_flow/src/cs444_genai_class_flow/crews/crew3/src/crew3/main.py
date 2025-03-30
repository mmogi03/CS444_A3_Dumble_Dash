#!/usr/bin/env python
import sys
import warnings
import json
from datetime import datetime

from crew3.crew import Crew3  # Changed from Crew2 to Crew3

# import litellm
# litellm._turn_on_debug()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'crew1_output': '''
        ### **Game Concept Document**

---

#### **Game Title:**
**"Arcane Depths"**

---

#### **Core Mechanics:**

1. **Card-Based Turn-Based Combat:**
   - **Deck Building:** Players construct a deck from a diverse pool of Arcane, Physical, and Elemental cards. Each card represents actions such as attacks, defenses, spells, and special abilities.
   - **Energy System:** Each turn, players have a limited energy pool to play cards, encouraging strategic decision-making on card usage.
   - **Card Synergies:** Combining specific cards can unlock powerful combo effects, promoting creative deck strategies.

2. **Roguelike Exploration:**
   - **Procedurally Generated Dungeons:** Each playthrough features uniquely generated levels with varying layouts, enemy placements, and environmental challenges.
   - **Permadeath:** Upon defeat, players lose their current progress but retain certain unlocks or upgrades for future runs, maintaining a sense of progression.
   - **Resource Management:** Players must manage limited resources such as health, mana, and items, adding strategic depth to exploration and combat.

3. **Level Crawling Elements:**
   - **Character Progression:** As players delve deeper into the Arcane Depths, they can unlock new cards, abilities, and upgrades to enhance their character.
   - **Environmental Interaction:** Levels include interactive elements like traps, hidden rooms, and environmental hazards that players must navigate using their card abilities.
   - **Boss Encounters:** Each dungeon culminates in a unique boss battle that tests the player's deck composition and tactical prowess.

---

#### **Replayability Features:**

1. **Procedural Generation:**
   - Every dungeon run presents a new combination of level layouts, enemy types, and item placements, ensuring no two playthroughs are the same.

2. **Diverse Card Pool and Deck Customization:**
   - With hundreds of unique cards available, players can experiment with countless deck combinations, tailoring their strategy to different playstyles and challenges.

3. **Unlockable Content:**
   - Completing runs and achieving specific milestones unlocks new cards, character classes, and abilities, providing ongoing goals and incentives to play multiple times.

4. **Dynamic Events and Challenges:**
   - Randomly occurring events such as time-limited challenges, special enemy encounters, and environmental changes keep gameplay fresh and engaging.

5. **Difficulty Scaling:**
   - Multiple difficulty levels and adaptive AI ensure that the game remains challenging for both new and experienced players, encouraging repeated attempts to master the game.

---

#### **Sample Starting Level and Enemy:**

**Level 1: "The Forgotten Crypt"**

*Description:*
Players begin their adventure in the "Forgotten Crypt," an ancient underground chamber shrouded in darkness and filled with lurking dangers. The air is thick with the scent of damp earth and old magic, and the flickering torchlight casts eerie shadows on the stone walls.

*Key Features:*
- **Layout:** A small, maze-like layout with multiple pathways, including hidden alcoves and one-way corridors that encourage exploration and strategic movement.
- **Environmental Hazards:** Occasional pressure plates trigger traps such as falling rocks or magical glyphs that temporarily disable certain card abilities.

**Enemy: "Crypt Shade"**

*Description:*
Crypt Shades are spectral entities that haunt the corridors of the Forgotten Crypt. They are elusive and attack with swift, ethereal strikes.

*Abilities:*
- **Shadow Strike:** A basic attack that deals moderate damage and has a chance to reduce the player's energy for the next turn.
- **Phantom Veil:** Allows the Crypt Shade to become intangible for one turn, avoiding all damage and repositioning on the battlefield.
- **Soul Drain (Boss Variation):** Attempts to drain the player's life force, healing the Crypt Shade and dealing heavy damage over time.

*Combat Mechanics:*
- **Turn Order:** Players and Crypt Shades take turns playing cards and executing actions based on their energy usage.
- **Strategic Positioning:** Players must position themselves to avoid traps while managing space to effectively use their card abilities against the Crypt Shades.
- **Card Synergy:** Utilizing cards that manipulate enemy actions or enhance defense can counteract the Crypt Shades' evasive tactics.

---

#### **Additional Features:**

- **Narrative Integration:**
  - A rich storyline unfolds through interactions with non-player characters, environmental storytelling, and card descriptions, immersing players in the lore of the Arcane Depths.

- **Competitive and Social Elements:**
  - Leaderboards allow players to compare their progress and high scores.
  - Cooperative multiplayer modes enable players to team up for special dungeon runs and challenges.

- **Mobile Accessibility:**
  - Designed with touch controls and optimized for mobile devices, ensuring smooth gameplay on the go without sacrificing depth or complexity.

---

**Conclusion:**
"Arcane Depths" seamlessly blends turn-based card combat with roguelike exploration and level crawling mechanics, providing a richly layered and highly replayable gaming experience. Through its deep deck customization, procedurally generated dungeons, and engaging narrative elements, the game offers endless strategic possibilities and immersive storytelling, appealing to both casual players and hardcore strategists alike.
        ''',

        'crew2_output': {
            "C:\\Users\\hazem\\Documents\\GitHub\\CS444_A3_Dumble_Dash\\cs444_genai_class_flow\\src\\cs444_genai_class_flow\\crews\\crew2\\outputs\\cryptic_echoes_105b91.mp3": "cryptic_echoes",
            "C:\\Users\\hazem\\Documents\\GitHub\\CS444_A3_Dumble_Dash\\cs444_genai_class_flow\\src\\cs444_genai_class_flow\\crews\\crew2\\outputs\\mystical_exploration_3880f0.mp3": "mystical_exploration",
            "C:\\Users\\hazem\\Documents\\GitHub\\CS444_A3_Dumble_Dash\\cs444_genai_class_flow\\src\\cs444_genai_class_flow\\crews\\crew2\\outputs\\triumphant_victory_45c59d.mp3": "triumphant_victory"
        }
    }

    try:
        Crew3().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Crew3().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Crew3().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        Crew3().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

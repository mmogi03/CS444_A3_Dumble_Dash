#!/usr/bin/env python
import warnings
from datetime import datetime
import sys
from pathlib import Path
import json

# Add the root of the project to the sys.path so imports resolve correctly
sys.path.append(str(Path(__file__).resolve().parent.parent))

from cs444_genai_class_flow.crews.crew1.crew import Crew1
from cs444_genai_class_flow.crews.crew2.crew import Crew2
from cs444_genai_class_flow.crews.crew3.crew import Crew3

from crewai.flow import Flow, start, listen
from pydantic import BaseModel

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

class BaseState(BaseModel):
    crew1_output: str = ""
    crew2_output: str = ""
    crew3_output: str = ""

class CrewsFlow(Flow[BaseState]):
    def __init__(self):
        super().__init__()
        print("CrewsFlow initialized")

    @start()
    def run_crew1(self):
        print("Running crew 1")
        crew1 = Crew1().crew()

        # Debug: show which tasks are loaded
        print("Tasks loaded into Crew1:")
        for task in crew1.tasks:
            print(f"- {task.description}")

        # Run the crew
        result = crew1.kickoff()

        # Debug: raw result and type
        print("Crew 1 raw result:", result)
        print("Crew 1 result type:", type(result))

        # Handle various possible result formats
        if result:
            if isinstance(result, list):
                print("Result is a list of task outputs:")
                for i, r in enumerate(result):
                    print(f"  Task {i+1} output:", r)
                self.state.crew1_output = "\n".join(map(str, result))

            elif isinstance(result, dict):
                print("Result is a dict of task outputs:")
                for k, v in result.items():
                    print(f"  {k}: {v}")
                self.state.crew1_output = "\n".join(f"{k}: {v}" for k, v in result.items())

            else:
                print("Result is a single object:", result)
                self.state.crew1_output = str(result)
        else:
            print("Crew 1 returned nothing")


    @listen(run_crew1)
    def run_crew2(self):
        print("Running crew 2")
        crew2 = Crew2().crew()
        result = crew2.kickoff(inputs = {"crew1_output": self.state.crew1_output})
        print("Crew 2 raw result:", result)
        print("Crew 2 result type:", type(result))

        if result:
            if isinstance(result, list):
                self.state.crew2_output = "\n".join(map(str, result))
            elif isinstance(result, dict):
                self.state.crew2_output = "\n".join(f"{k}: {v}" for k, v in result.items())
            else:
                self.state.crew2_output = str(result)
        else:
            print("Crew 2 returned nothing")

    @listen(run_crew2)
    def run_crew3(self):
        print("Running crew 3")
        
        asset_map_path = "outputs/asset_mapping.json"
        print("Loading asset_map from Crew2...")
        with open(asset_map_path, "r") as f:
            asset_map = json.load(f)
            
        print("asset_map loaded from Crew2: ", asset_map)
        
        result = (
            Crew3().crew().kickoff(inputs = {"crew1_output": self.state.crew1_output , "crew2_output": self.state.crew2_output, 
                                   "base_template": '''
                                   <!DOCTYPE html>
                                   <html>
                                   <head>
                                    <meta charset="utf-8" />
                                    <meta content="width=device-width, initial-scale=1.0, user-scalable=no" name="viewport" />
                                    <title>Generated Game</title>
                                    <style>
                                    body, html {
                                            margin: 0;
                                            padding: 0;
                                            height: 100%;
                                            font-family: 'Orbitron', sans-serif;
                                            background-color: #1a1a2e;
                                            color: #ffffff;
                                        }
                                        .screen {
                                            display: none;
                                            height: 100%;
                                            width: 100%;
                                            position: absolute;
                                            top: 0;
                                            left: 0;
                                            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                                        }
                                        .screen.active {
                                            display: flex;
                                            flex-direction: column;
                                            justify-content: center;
                                            align-items: center;
                                        }
                                        .container {
                                            text-align: center;
                                            max-width: 600px;
                                            width: 90%;
                                        }
                                        button {
                                            background: linear-gradient(135deg, #283c86 0%, #45a247 100%);
                                            border: 2px solid #fff;
                                            border-radius: 8px;
                                            color: #fff;
                                            font-family: 'Orbitron', sans-serif;
                                            font-size: 18px;
                                            text-transform: uppercase;
                                            text-align: center;
                                            text-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
                                            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
                                            padding: 12px 30px;
                                            margin: 20px auto 0;
                                            display: block;
                                            width: 215.15px;
                                            cursor: pointer;
                                            transition: all 0.3s ease;
                                        }
                                        button:hover {
                                            background: linear-gradient(135deg, #45a247 0%, #283c86 100%);
                                            transform: translateY(-2px);
                                            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
                                        }
                                        #game-title {
                                            font-size: 2.5em;
                                            margin-bottom: 30px;
                                            text-transform: uppercase;
                                            text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
                                            color: #e94560;
                                        }
                                        #game-controls {
                                            position: fixed;
                                            top: 0;
                                            left: 0;
                                            width: 100%;
                                            background-color: rgba(26, 26, 46, 0.8);
                                            padding: 10px 0; /* Changed padding */
                                            z-index: 101;
                                            display: none;
                                            text-align: center; /* Center align the content */
                                        }
                                        #game-controls button {
                                            display: inline-block;
                                            width: auto;
                                            padding: 8px 15px;
                                            margin: 0 5px; /* Reduced side margins */
                                            font-size: 14px;
                                        }
                                        #hud {
                                            position: fixed;
                                            top: 50px;
                                            left: 0;
                                            width: 100%;
                                            background-color: rgba(255, 255, 255, 0.9);
                                            color: #1a1a2e;
                                            padding: 10px;
                                            z-index: 100;
                                            display: none;
                                            font-family: 'Orbitron', sans-serif;
                                            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
                                        }
                                        #game-container {
                                            position: relative;
                                            width: 100%;
                                            height: calc(100% - 100px);
                                            overflow: hidden;
                                            background-color: #0f3460;
                                            border: 2px solid #e94560;
                                            box-shadow: 0 0 20px rgba(233, 69, 96, 0.5);
                                        }
                                        #game-screen {
                                            background: none;
                                        }
                                        #instructions-screen {
                                            z-index: 200;
                                        }
                                        #instructions-screen.overlay {
                                            background: rgba(0, 0, 0, 0.8);
                                        }
                                        #instructions-screen .container {
                                            background: #1a1a2e;
                                            padding: 20px;
                                            border-radius: 10px;
                                            box-shadow: 0 0 20px rgba(233, 69, 96, 0.5);
                                        }
                                        @media (max-width: 600px) {
                                            #game-title {
                                                font-size: 2em;
                                            }
                                            button {
                                                width: 80%;
                                                font-size: 16px;
                                            }
                                            #game-controls button {
                                                font-size: 12px;
                                                padding: 6px 12px;
                                            }
                                        }
                                        
                                        <!--Your style goes here -->
                                        
                                    </style>
                                </head>
                                <body>
                                    <div id="game-controls">
                                        <button id="game-menu-button">Menu</button>
                                        <button id="game-restart-button">Restart</button>
                                        <button id="game-instructions-button">Instructions</button>
                                    </div>
                                    <!-- Use HUD for Score, High Score, and Other Game Information -->
                                    <div id="hud"></div>

                                    <div id="start-menu-screen" class="active screen">
                                        <div class="container">
                                            <h1 id="game-title">Your Game Title</h1>
                                            <button id="play-button">Play</button>
                                            <button id="settings-button">Settings</button>
                                            <button id="instructions-button">Instructions</button>
                                        </div>
                                    </div>

                                    <div id="settings-screen" class="screen">
                                        <div class="container">
                                            <h2>Settings</h2>
                                            <!-- Add settings options here -->
                                            <button id="settings-back-button">Back</button>
                                        </div>
                                    </div>

                                    <div id="instructions-screen" class="screen">
                                        <div class="container">
                                            <h2>Instructions</h2>
                                            <h3>How to Play:</h3>
                                            <ul>
                                                <li>Instruction 1</li>
                                                <li>Instruction 2</li>
                                            </ul>
                                            <h3>Controls:</h3>
                                            <ul>
                                                <li>Control 1</li>
                                                <li>Control 2</li>
                                            </ul>
                                            <button id="instructions-back-button">Back</button>
                                        </div>
                                    </div>

                                    <div id="game-screen" class="screen">
                                        <div id="game-container"></div>
                                    </div>

                                    <div id="game-over-screen" class="screen">
                                        <div class="container">
                                            <div id="game-over-message"></div>
                                            <button id="play-again-button">Play Again</button>
                                            <button id="main-menu-button">Main Menu</button>
                                        </div>
                                    </div>
                                    <audio autoplay="" id="background-music" loop="">
                                    <source src="background-music.mp3" type="audio/mpeg" />
                                    </audio>
                                    <audio id="start-game-sound">
                                    <source src="start-game-sound.mp3" type="audio/mpeg" />
                                    </audio>
                                    <!--Extra audio tags for sound effects-->
                                    
                                    <!--You will create your own scripts in the following files-->    
                                    <script>
                                    document.addEventListener('DOMContentLoaded', () => {
                                        class GameUI {
                                        constructor() {
                                            this.startMenuScreen = document.getElementById('start-menu-screen');
                                            this.settingsScreen = document.getElementById('settings-screen');
                                            this.instructionsScreen = document.getElementById('instructions-screen');
                                            this.gameContainer = document.getElementById('game-screen');
                                            this.gameOverScreen = document.getElementById('game-over-screen');
                                            this.gameControls = document.getElementById('game-controls');
                                            this.hud = document.getElementById('hud');
                                        };
                                        
                                        
                                        swapToScreen(screen) {
                                            this.startMenuScreen.classList.remove('active');
                                            this.settingsScreen.classList.remove('active');
                                            this.instructionsScreen.classList.remove('active');
                                            this.gameContainer.classList.remove('active');
                                            this.gameOverScreen.classList.remove('active');
                                            screen.classList.add('active');			
                                            
                                            if (screen.id === 'game-screen') {
                                                this.hud.style.display = 'block';
                                                this.gameControls.style.display = 'block';
                                            } else {
                                                this.hud.style.display = 'none';
                                                this.gameControls.style.display = 'none';
                                            }
                                        };
                                        
                                        startGame() {
                                            const startGameSound = document.getElementById('start-game-sound');
                                            this.swapToScreen(this.gameContainer);
                                            startGameSound.play();
                                            // Your start game code here;
                                        }
                                        
                                        endGame() {
                                            const endGameSound = document.getElementById('end-game-sound');
                                            this.swapToScreen(this.gameOverScreen);
                                            endGameSound.play();
                                            // Your end game code here;
                                        }
                                        
                                        mainMenu() {
                                            this.swapToScreen(this.startMenuScreen);
                                        }
                                        
                                        playAgain() {
                                            this.swapToScreen(this.gameContainer);
                                        }
                                        
                                        settings() {
                                            this.swapToScreen(this.settingsScreen);
                                        }
                                        
                                        instructions() {
                                            this.swapToScreen(this.instructionsScreen);
                                        }		  
                                        
                                        // Your UI functions here;
                                        
                                        }
                                        class GameLogic {
                                        constructor() {
                                        }
                                        // Your game logic here;
                                        }
                                        class Game {
                                        constructor() {
                                            this.ui = new GameUI();
                                            this.logic = new GameLogic();
                                            this.lastFrameTime = 0;
                                            this.updateInterval = 1000 / 60;
                                            this.done = false;
                                            this.isPaused = false;
                                            this.animationFrameId = null;
                                        }
                                        prepareGame() {
                                            const gameContainer = document.getElementById('game-screen');
                                            // Prepare game container DOM elements here;            
                                            // Connect DOM element to game logic or game ui accordingly;
                                            this.assignButtons();
                                        }
                                        startGame() {
                                            this.ui.startGame();
                                            // Start game logic here;
                                            
                                            // this.updateInterval = /* Your desired update interval */;
                                            
                                            if(this.animationFrameId)
                                            {
                                                cancelAnimationFrame(this.animationFrameId);
                                            }
                                            this.animationFrameId = requestAnimationFrame(this.gameLoop.bind(this));
                                        }
                                        updateGame() {
                                            // Update game logic here;
                                        }
                                        resetGame() {
                                            // Reset game logic here;			
                                            this.isPaused = false;
                                            cancelAnimationFrame(this.animationFrameId);
                                        }
                                        pause() {
                                            this.isPaused = true;
                                            cancelAnimationFrame(this.animationFrameId);
                                        }
                                        resume() {
                                            this.isPaused = false;
                                            this.gameLoop();
                                        }
                                        gameLoop(timestamp) {
                                            if (this.done) return;
                                            const deltaTime = timestamp - this.lastFrameTime;
                                            if (deltaTime > this.updateInterval) {
                                            this.updateGame();
                                            this.lastFrameTime = timestamp;
                                            }
                                            if(this.animationFrameId)
                                            {
                                                cancelAnimationFrame(this.animationFrameId);
                                            }
                                            this.animationFrameId = requestAnimationFrame(this.gameLoop.bind(this));
                                        }
                                        assignButtons() {
                                            const playButton = document.getElementById('play-button');
                                            const settingsButton = document.getElementById('settings-button');
                                            const instructionsButton = document.getElementById('instructions-button');
                                            const playAgainButton = document.getElementById('play-again-button');
                                            const mainMenuButtons = document.querySelectorAll('#game-over-main-menu-button, #settings-back-button, #instructions-back-button');
                                            const gameMenuButton = document.getElementById('game-menu-button');
                                            const gameRestartButton = document.getElementById('game-restart-button');
                                            const gameInstructionsButton = document.getElementById('game-instructions-button');

                                            playButton.addEventListener('click', this.startGame.bind(this));
                                            settingsButton.addEventListener('click', this.ui.settings.bind(this.ui));
                                            instructionsButton.addEventListener('click', this.ui.instructions.bind(this.ui));
                                            playAgainButton.addEventListener('click', this.startGame.bind(this));
                                            mainMenuButtons.forEach(button => button.addEventListener('click', () => {
                                                this.ui.mainMenu();
                                            }));
                                            gameMenuButton.addEventListener('click', () => {
                                                this.ui.mainMenu();
                                            });
                                            gameRestartButton.addEventListener('click', this.startGame.bind(this));
                                            gameInstructionsButton.addEventListener('click', () => {
                                                        this.pause();						
                                                        this.ui.swapToScreen(this.ui.instructionsScreen);
                                                        document.getElementById('instructions-back-button').addEventListener('click', () => {
                                                            this.ui.swapToScreen(this.ui.gameContainer);
                                                            this.resume();
                                                        }, { once: true });
                                                    });
                                            
                                            // Your button event listeners here
                                        }
                                        }
                                        const game = new Game();
                                        game.prepareGame();
                                    });
                                    </script>
                                </body>
                                </html> ''' , "asset_map": asset_map, 
                                "main_js": ''' 
// src/main.js
// Entry point: sets up the Phaser game, imports scenes & utilities, and manages DOM events

import BootScene from "./src/scenes/BootScene.js";
import OverworldScene from "./src/scenes/OverworldScene.js";
import { fadeAudio } from "./src/utils/audio.js";
import { updateHealthBar, updateManaBar, updateLevelText, updateScoreText } from "./src/utils/ui.js";
import { castSpell, doEnemyTurn } from "./src/utils/battle.js";

// Global game state
window.isGameActive = false;
window.currentDifficulty = 'easy';
window.currentTurn = 'none';
window.playerPoints = 0;
window.score = 0;

// Phaser game configuration
const config = {
  type: Phaser.AUTO,
  parent: "game-container",
  width: window.innerWidth,
  height: window.innerHeight - 64,
  scale: {
    mode: Phaser.Scale.RESIZE,
    autoCenter: Phaser.Scale.CENTER_BOTH
  },
  physics: {
    default: "arcade",
    arcade: { debug: false }
  },
  scene: []
};

const game = new Phaser.Game(config);
window.game = game; // Make available globally for utility access
game.scene.add("BootScene", BootScene);
game.scene.add("OverworldScene", OverworldScene);

document.addEventListener("DOMContentLoaded", () => {
  const startGameMusic = document.getElementById("start-game-sound");
  startGameMusic.volume = 1;
  startGameMusic.play().catch((err) => console.log("Auto-play blocked:", err));

  const playButton = document.getElementById("play-button");
  const settingsButton = document.getElementById("settings-button");
  const instructionsButton = document.getElementById("instructions-button");
  const settingsBackButton = document.getElementById("settings-back-button");
  const instructionsBackButton = document.getElementById("instructions-back-button");
  const playAgainButton = document.getElementById("play-again-button");
  const mainMenuButton = document.getElementById("main-menu-button");
  const gameMenuButton = document.getElementById("game-menu-button");
  const gameRestartButton = document.getElementById("game-restart-button");
  const gameInstructionsButton = document.getElementById("game-instructions-button");
  const startMenuScreen = document.getElementById("start-menu-screen");
  const settingsScreen = document.getElementById("settings-screen");
  const instructionsScreen = document.getElementById("instructions-screen");
  const gameScreen = document.getElementById("game-screen");
  const gameOverScreen = document.getElementById("game-over-screen");

  function showScreen(scr) {
    [startMenuScreen, settingsScreen, instructionsScreen, gameScreen, gameOverScreen].forEach((s) => s.classList.remove("active"));
    if (scr) scr.classList.add("active");
  }

  // Play Button: resume if active; else start new game
  playButton.addEventListener("click", () => {
    if (window.isGameActive) {
      showScreen(gameScreen);
      if (game.scene.isPaused("OverworldScene")) {
        game.scene.resume("OverworldScene");
      }
    } else {
      fadeAudio(startGameMusic, 0, 1000, () => {
        startGameMusic.pause();
        startGameMusic.currentTime = 0;
        showScreen(gameScreen);
        game.scene.start("BootScene");
        window.isGameActive = true;
      });
    }
  });

  settingsButton.addEventListener("click", () => showScreen(settingsScreen));
  instructionsButton.addEventListener("click", () => showScreen(instructionsScreen));

  settingsBackButton.addEventListener("click", () => {
    if (window.isGameActive) {
      showScreen(gameScreen);
      if (game.scene.isPaused("OverworldScene")) {
        game.scene.resume("OverworldScene");
      }
    } else {
      showScreen(startMenuScreen);
    }
  });

  instructionsBackButton.addEventListener("click", () => {
    if (window.isGameActive) {
      showScreen(gameScreen);
      if (game.scene.isPaused("OverworldScene")) {
        game.scene.resume("OverworldScene");
      }
    } else {
      showScreen(startMenuScreen);
    }
  });

  playAgainButton.addEventListener("click", () => {
    showScreen(gameScreen);
    window.isGameActive = true;
    game.scene.start("OverworldScene");
  });

  mainMenuButton.addEventListener("click", () => {
    showScreen(startMenuScreen);
    window.isGameActive = false;
  });

  gameMenuButton.addEventListener("click", () => {
    showScreen(startMenuScreen);
    game.scene.pause("OverworldScene");
  });

  // Updated Restart Button: hide battle UI (if visible) when restart is pressed
  gameRestartButton.addEventListener("click", () => {
    showScreen(gameScreen);
    // Hide the battle UI regardless of battle state
    const battleUI = document.getElementById("battle-ui");
    if (battleUI) battleUI.style.display = "none";
    window.isGameActive = true;
    game.scene.start("OverworldScene");
  });

  gameInstructionsButton.addEventListener("click", () => {
    showScreen(instructionsScreen);
  });

  // Battle UI event bindings
  const fireballCard = document.getElementById("fireball-card");
  const mudwallCard = document.getElementById("mudwall-card");
  const healCard = document.getElementById("heal-card");
  const skipTurnButton = document.getElementById("skip-turn-button");

  fireballCard.addEventListener("click", () => castSpell("fireball"));
  mudwallCard.addEventListener("click", () => castSpell("mudWall"));
  healCard.addEventListener("click", () => castSpell("astralHeal"));
  skipTurnButton.addEventListener("click", () => {
    window.currentTurn = "enemy";
    doEnemyTurn();
  });
});
''', 
"index_html":'''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>DumbleDash 2D (Phaser Version)</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
    <link rel="icon" href="assets/textures/DumbleDashIcon.png" />
    <script src="https://cdn.jsdelivr.net/npm/phaser@3.60.0/dist/phaser.min.js"></script>
    <style>
        html, body {
          margin: 0;
          padding: 0;
          width: 100%;
          height: 100%;
          font-family: 'Orbitron', sans-serif;
          background-color: #1a1a2e;
          color: #ffffff;
          overflow: hidden;
        }
        .screen {
          display: none;
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          justify-content: center;
          align-items: center;
          background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
          z-index: 999999;
          text-align: center;
        }
        .screen.active {
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
        }
        .container {
          text-align: center;
          max-width: 600px;
          width: 90%;
          margin: 0 auto;
        }
        button {
          background: linear-gradient(135deg, #283c86 0%, #45a247 100%);
          border: 2px solid #fff;
          border-radius: 8px;
          color: #fff;
          font-family: 'Orbitron', sans-serif;
          font-size: 18px;
          text-transform: uppercase;
          text-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
          box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
          padding: 12px 30px;
          margin: 20px auto 0;
          display: block;
          width: 215px;
          cursor: pointer;
          transition: all 0.3s ease;
        }
        button:hover {
          background: linear-gradient(135deg, #45a247 0%, #283c86 100%);
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }
        #game-title {
          font-size: 2.5em;
          margin-bottom: 30px;
          text-transform: uppercase;
          text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
          color: #e94560;
        }
        #game-screen {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          display: none;
          background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        }
        #game-screen.active {
          display: block;
        }
        #game-controls {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 60px;
          background-color: rgba(26, 26, 46, 0.8);
          padding: 10px 0;
          z-index: 101;
          text-align: center;
        }
        #game-controls button {
          display: inline-block;
          width: auto;
          padding: 8px 15px;
          margin: 0 5px;
          font-size: 14px;
        }
        #game-container {
          position: absolute;
          top: 60px;
          left: 0;
          width: calc(100% - 4px);
          height: calc(100% - 220px - 4px);
          border: 2px solid #e94560;
          box-sizing: border-box;
          overflow: hidden;
          background-color: #0f3460;
          box-shadow: 0 0 20px rgba(233, 69, 96, 0.5);
        }
        #hud {
          position: absolute;
          top: 70px;
          left: 10px;
          color: #fff;
          z-index: 101;
          font-family: 'Orbitron', sans-serif;
        }
        #health-bar, #mana-bar {
          width: 300px;
          height: 24px;
          background-color: rgba(50, 50, 50, 0.8);
          border: 2px solid #222;
          border-radius: 12px;
          box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.5);
          margin: 10px 0;
          overflow: hidden;
        }
        #health-fill, #mana-fill {
          width: 100%;
          height: 100%;
          transition: width 0.5s ease;
        }
        #health-fill {
          background: linear-gradient(to right, #4CAF50, #2E8B57);
        }
        #mana-fill {
          background: linear-gradient(to right, #0000FF, #0000AA);
        }
        #enemy-health-bar {
          position: fixed;
          top: 70px;
          right: 10px;
          width: 300px;
          height: 24px;
          background-color: rgba(50,50,50,0.8);
          border: 2px solid #222;
          border-radius: 12px;
          overflow: hidden;
          display: none;
        }
        #enemy-health-fill {
          width: 100%;
          height: 100%;
          background: linear-gradient(to right, #FF0000, #AA0000);
        }
        #battle-ui {
          position: absolute;
          bottom: 20%;
          left: 50%;
          transform: translate(-50%, -50%);
          width: 400px;
          height: 200px;
          background: rgba(0, 0, 0, 0.5);
          z-index: 9999999999;
          display: none;
          flex-direction: column;
          justify-content: space-between;
          align-items: center;
          padding: 10px;
        }
        #battle-ui .card-container img {
          width: 100px;
          height: auto;
          margin: 0 10px;
        }
        #game-over-screen {
          display: none;
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          justify-content: center;
          align-items: center;
          background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
          z-index: 999999;
          text-align: center;
        }
        #game-over-screen.active {
          display: flex;
        }
        #game-over-message {
          font-size: 72px;
          font-weight: bold;
          color: #ff4d4d;
          margin-bottom: 20px;
          letter-spacing: 3px;
          text-shadow:
            -1.5px -1.5px 0 #000, 1.5px -1.5px 0 #000,
            -1.5px 1.5px 0 #000, 1.5px 1.5px 0 #000,
            0 0 15px rgba(255, 77, 77, 0.8),
            0 0 30px rgba(255, 0, 0, 0.6);
        }
        #level-score {
          margin-top: 10px;
          font-size: 20px;
        }
        @media (max-width: 600px) {
          #game-title {
            font-size: 2em;
          }
          button {
            width: 80%;
            font-size: 16px;
          }
          #game-controls button {
            font-size: 12px;
            padding: 6px 12px;
          }
          #health-bar, #mana-bar {
            width: 80%;
            max-width: 300px;
          }
        }
      </style>
  </head>
  <body>
    <div id="start-menu-screen" class="screen active">
      <div class="container">
        <h1 id="game-title">Dumble Dash</h1>
        <button id="play-button">Play</button>
        <button id="settings-button">Settings</button>
        <button id="instructions-button">Instructions</button>
      </div>
    </div>
    <div id="settings-screen" class="screen">
      <div class="container">
        <h2>Settings</h2>
        <div id="difficulty-options">
          <label><input type="radio" name="difficulty" value="easy" checked />Easy</label>
          <label><input type="radio" name="difficulty" value="medium" />Medium</label>
          <label><input type="radio" name="difficulty" value="hard" />Hard</label>
        </div>
        <label for="volume-slider">Game Volume</label>
        <input type="range" id="volume-slider" min="0" max="1" step="0.1" value="1" />
        <button id="settings-back-button">Back</button>
      </div>
    </div>
    <div id="instructions-screen" class="screen">
      <div class="container">
        <div class="instructions-wrapper">
          <h2>Instructions</h2>
          <h3>How to Play:</h3>
          <ul>
            <li>Fight off enemies of the Forsaken Order as DumbleWall!</li>
            <li>Click on spells to attack. Different spells do different damage.</li>
          </ul>
          <h3>Controls:</h3>
          <ul>
            <li>WASD to move (top-down).</li>
            <li>E to interact.</li>
            <li>Shift to sprint.</li>
          </ul>
        </div>
        <button id="instructions-back-button">Back</button>
      </div>
    </div>
    <div id="game-screen" class="screen">
      <div id="game-controls">
        <button id="game-menu-button">Menu</button>
        <button id="game-restart-button">Restart</button>
        <button id="game-instructions-button">Instructions</button>
      </div>
      <div id="game-container"></div>
      <div id="hud">
        <div id="health-bar"><div id="health-fill"></div></div>
        <div id="mana-bar"><div id="mana-fill"></div></div>
        <div id="level-score">
          <div id="level-text">Level: 1</div>
          <div id="score-text">Score: 0</div>
        </div>
      </div>
      <div id="enemy-health-bar">
        <div id="enemy-health-fill"></div>
      </div>
      <div id="battle-ui">
        <div class="card-container">
          <img id="fireball-card" src="assets/textures/Fireball.png" />
          <img id="mudwall-card" src="assets/textures/MudWall.png" />
          <img id="heal-card" src="assets/textures/AstralHeal.png" />
        </div>
        <button id="skip-turn-button">Skip Turn</button>
      </div>
    </div>
    <div id="game-over-screen" class="screen">
      <div class="container">
        <div id="game-over-message">You Died!</div>
        <button id="play-again-button">Play Again</button>
        <button id="main-menu-button">Main Menu</button>
      </div>
    </div>
    <audio autoplay id="background-music" loop>
      <source src="assets/music/background_music_1.mp3" type="audio/mpeg" />
    </audio>
    <audio id="start-game-sound" loop>
      <source src="assets/music/start_game_music.mp3" type="audio/mpeg" />
    </audio>
    <audio id="end-game-music">
      <source src="assets/music/end_game_music.mp3" type="audio/mpeg" />
    </audio>
    <script type="module" src="main.js"></script>
  </body>
</html>
''', "audio_js": '''
// src/utils/audio.js
export function setGlobalVolume(vol) {
    const audioElements = [
      document.getElementById("background-music"),
      document.getElementById("start-game-sound"),
      document.getElementById("end-game-music"),
      window.castleCutsceneBgm,
      window.castleCutsceneAudio
    ];
    audioElements.forEach((audio) => {
      if (audio) audio.volume = vol;
    });
  }
  
  export function fadeAudio(audio, targetVolume, duration, callback) {
    if (!audio) return;
    const initialVolume = audio.volume;
    const startTime = performance.now();
    function tick() {
      const elapsed = performance.now() - startTime;
      const fraction = Math.min(elapsed / duration, 1);
      audio.volume = initialVolume + (targetVolume - initialVolume) * fraction;
      if (fraction < 1) {
        requestAnimationFrame(tick);
      } else if (callback) {
        callback();
      }
    }
    tick();
  }
''', "battle_js":'''
// src/utils/battle.js
import { updateManaBar, updateHealthBar, updateEnemyHealthBar, updateScoreText, showBattleUI } from "./ui.js";
import { fadeAudio } from "./audio.js";

export const SpellCosts = {
  fireball: 3,
  mudWall: 1,
  astralHeal: 3
};

export function castSpell(spellName) {
  const scene = getCurrentScene();
  if (!scene) return;
  if (scene.playerMana < SpellCosts[spellName]) {
    console.log("Not enough mana!");
    return;
  }
  if (spellName === "astralHeal" && scene.playerHealth >= scene.playerMaxHealth) {
    console.log("Already at full HP!");
    return;
  }
  scene.playerMana -= SpellCosts[spellName];
  updateManaBar(scene.playerMana, scene.playerMaxMana);
  // Hide battleUI immediately
  document.getElementById("battle-ui").style.display = "none";
  if (spellName === "fireball") {
    scene.currentEnemy.setTint(0xffaaaa);
    scene.enemyHealth -= 2;
    updateEnemyHealthBar(scene.enemyHealth, scene.enemyMaxHealth);
    if (scene.enemyHealth <= 0) {
      scene.time.delayedCall(1000, () => {
        if (scene.currentEnemy) scene.currentEnemy.clearTint();
        endBattle(scene, true);
      });
      return;
    } else {
      scene.time.delayedCall(1000, () => {
        if (scene.currentEnemy) scene.currentEnemy.clearTint();
        window.currentTurn = "enemy";
        doEnemyTurn();
      });
      return;
    }
  } else if (spellName === "mudWall") {
    scene.currentEnemy.setTint(0xffaaaa);
    scene.enemyHealth -= 1;
    updateEnemyHealthBar(scene.enemyHealth, scene.enemyMaxHealth);
    if (scene.enemyHealth <= 0) {
      scene.time.delayedCall(1000, () => {
        if (scene.currentEnemy) scene.currentEnemy.clearTint();
        endBattle(scene, true);
      });
      return;
    } else {
      scene.time.delayedCall(1000, () => {
        if (scene.currentEnemy) scene.currentEnemy.clearTint();
        window.currentTurn = "enemy";
        doEnemyTurn();
      });
      return;
    }
  } else if (spellName === "astralHeal") {
    scene.playerHealth = Math.min(scene.playerMaxHealth, scene.playerHealth + 5);
    updateHealthBar(scene.playerHealth, scene.playerMaxHealth);
    scene.time.delayedCall(500, () => {
      window.currentTurn = "enemy";
      doEnemyTurn();
    });
  }
}

export function doEnemyTurn() {
  const scene = getCurrentScene();
  if (!scene) return;
  // Ensure battleUI is hidden
  document.getElementById("battle-ui").style.display = "none";
  scene.time.delayedCall(500, () => {
    const gameContainer = document.getElementById("game-container");
    if (gameContainer) {
      const overlay = document.createElement("div");
      overlay.style.position = "absolute";
      overlay.style.top = "0";
      overlay.style.left = "0";
      overlay.style.width = "100%";
      overlay.style.height = "100%";
      overlay.style.backgroundColor = "rgba(255, 0, 0, 0.3)";
      overlay.style.pointerEvents = "none";
      overlay.id = "damage-overlay";
      gameContainer.appendChild(overlay);
      setTimeout(() => {
        overlay.remove();
      }, 1000);
    }
    // Pause before processing enemy damage
    scene.time.delayedCall(1000, () => {
      scene.playerHealth -= 1;
      if (scene.playerHealth <= 0) {
        scene.playerHealth = 0;
        updateHealthBar(scene.playerHealth, scene.playerMaxHealth);
        showGameOver();
      } else {
        updateHealthBar(scene.playerHealth, scene.playerMaxHealth);
        scene.playerMana = Math.min(scene.playerMaxMana, scene.playerMana + 1);
        updateManaBar(scene.playerMana, scene.playerMaxMana);
        window.currentTurn = "player";
        document.getElementById("battle-ui").style.display = "flex";
      }
    });
  });
}

export function endBattle(scene, playerWon) {
  window.inBattle = false;
  window.currentTurn = "none";
  document.getElementById("battle-ui").style.display = "none";
  document.getElementById("enemy-health-bar").style.display = "none";
  if (playerWon && scene.currentEnemy) {
    scene.currentEnemy.redOutline.destroy();
    Phaser.Utils.Array.Remove(scene.enemies, scene.currentEnemy);
    scene.currentEnemy.destroy();
    scene.currentEnemy = null;
    window.score += 100;
    updateScoreText();
  }
}

export function showGameOver() {
  document.getElementById("game-over-screen").classList.add("active");
  document.getElementById("hud").style.display = "none";
  document.getElementById("game-controls").style.display = "none";
  const bgMusic = document.getElementById("background-music");
  fadeAudio(bgMusic, 0, 2000, () => {
    bgMusic.pause();
    bgMusic.currentTime = 0;
  });
  const endMusic = document.getElementById("end-game-music");
  if (endMusic) {
    endMusic.volume = 0;
    endMusic.play().then(() => fadeAudio(endMusic, 1, 1000));
  }
}

export function getCurrentScene() {
  if (window.game && window.game.scene.isActive("OverworldScene")) {
    return window.game.scene.getScene("OverworldScene");
  }
  return null;
}
''', "maze_js": '''
// src/utils/maze.js
export function generateMaze(width, height) {
    const maze = [];
    for (let y = 0; y < height; y++) {
      maze[y] = [];
      for (let x = 0; x < width; x++) {
        maze[y][x] = 1;
      }
    }
    function shuffle(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
      return array;
    }
    function carve(x, y) {
      maze[y][x] = 0;
      const directions = shuffle([[0, -2], [2, 0], [0, 2], [-2, 0]]);
      for (let [dx, dy] of directions) {
        const nx = x + dx;
        const ny = y + dy;
        if (nx > 0 && nx < width && ny > 0 && ny < height && maze[ny][nx] === 1) {
          maze[y + dy / 2][x + dx / 2] = 0;
          carve(nx, ny);
        }
      }
    }
    carve(1, 1);
    for (let y = 1; y < height - 1; y++) {
      for (let x = 1; x < width - 1; x++) {
        if (maze[y][x] === 1 && Math.random() < 0.1) {
          maze[y][x] = 0;
        }
      }
    }
    return maze;
  }
  
  export function getOpenCells(maze) {
    const openCells = [];
    for (let y = 0; y < maze.length; y++) {
      for (let x = 0; x < maze[y].length; x++) {
        if (maze[y][x] === 0) {
          openCells.push({ x, y });
        }
      }
    }
    return openCells;
  }
''', "ui_js": '''

// src/utils/ui.js
export function updateHealthBar(current, max) {
    const pct = (current / max) * 100;
    const healthFill = document.getElementById("health-fill");
    if (healthFill) healthFill.style.width = pct + "%";
  }
  
  export function updateManaBar(current, max) {
    const pct = (current / max) * 100;
    const manaFill = document.getElementById("mana-fill");
    if (manaFill) manaFill.style.width = pct + "%";
  }
  
  export function updateEnemyHealthBar(current, max) {
    const pct = (current / max) * 100;
    const enemyHealthFill = document.getElementById("enemy-health-fill");
    if (enemyHealthFill) enemyHealthFill.style.width = pct + "%";
  }
  
  export function showBattleUI(flag) {
    const battleUI = document.getElementById("battle-ui");
    if (battleUI) {
      battleUI.style.display = flag ? "flex" : "none";
    }
  }
  
  export function updateLevelText() {
    const levelText = document.getElementById("level-text");
    if (levelText) levelText.innerText = "Level: " + window.currentLevel;
  }
  
  export function updateScoreText() {
    const scoreText = document.getElementById("score-text");
    if (scoreText) scoreText.innerText = "Score: " + window.score;
  }
''', "BootScene_js":'''
// src/scenes/BootScene.js
export default class BootScene extends Phaser.Scene {
    constructor() {
      super("BootScene");
    }
    preload() {
      this.load.image("player", "assets/textures/wizardface.webp");
      this.load.image("enemy", "assets/textures/enemyface.webp");
      this.load.image("castle", "assets/castle.png");
      this.load.image("ground", "assets/textures/dungeon_floor.jpg");
      this.load.image("wall", "assets/textures/brick_diffuse.jpg");
    }
    create() {
      this.scene.start("OverworldScene");
    }
  }
''', "OverworldScene_js": '''
// src/scenes/OverworldScene.js
import { fadeAudio } from "../utils/audio.js";
import { updateHealthBar, updateManaBar, updateLevelText, updateScoreText, updateEnemyHealthBar, showBattleUI } from "../utils/ui.js";
import { generateMaze, getOpenCells } from "../utils/maze.js";

export default class OverworldScene extends Phaser.Scene {
  constructor() {
    super("OverworldScene");
    this.levelCompleted = false;
  }
  create() {
    if (!window.currentLevel) window.currentLevel = 1;
    this.levelCompleted = false;

    const gameWidth = this.game.config.width;
    const gameHeight = this.game.config.height;
    const baseTileSize = 40;
    const columns = Math.floor(gameWidth / baseTileSize);
    const rows = Math.round(columns * (gameHeight / gameWidth));
    const tileSize = Math.min(gameWidth / columns, gameHeight / rows);

    this.lights.enable();
    this.lights.setAmbientColor(0x000000);

    const maze = generateMaze(columns, rows);
    this.groundGroup = this.add.group();
    this.wallsGroup = this.physics.add.staticGroup();
    for (let y = 0; y < rows; y++) {
      for (let x = 0; x < columns; x++) {
        const worldX = x * tileSize;
        const worldY = y * tileSize;
        const groundTile = this.groundGroup.create(worldX + tileSize / 2, worldY + tileSize / 2, "ground");
        groundTile.setDisplaySize(tileSize, tileSize);
        groundTile.setPipeline("Light2D");
        if (maze[y][x] === 1) {
          const wallTile = this.wallsGroup.create(worldX + tileSize / 2, worldY + tileSize / 2, "wall");
          wallTile.setDisplaySize(tileSize, tileSize);
          wallTile.refreshBody();
          wallTile.setPipeline("Light2D");
        }
      }
    }
    this.physics.world.setBounds(0, 0, gameWidth, gameHeight);
    this.cameras.main.setBounds(0, 0, gameWidth, gameHeight);
    this.cameras.main.setBackgroundColor("#0f3460");

    const openCells = getOpenCells(maze);
    const playerCell = Phaser.Utils.Array.GetRandom(openCells);
    this.player = this.physics.add.sprite(
      playerCell.x * tileSize + tileSize / 2,
      playerCell.y * tileSize + tileSize / 2,
      "player"
    );
    this.player.setDisplaySize(tileSize * 0.8, tileSize * 0.8);
    this.player.setCollideWorldBounds(true);
    this.player.setPipeline("Light2D");
    this.physics.add.collider(this.player, this.wallsGroup);

    this.enemies = [];
    const enemyCells = openCells.filter(cell => !(cell.x === playerCell.x && cell.y === playerCell.y));
    const numEnemies = window.currentLevel + 1;
    for (let i = 0; i < numEnemies; i++) {
      if (enemyCells.length === 0) break;
      const enemyCell = Phaser.Utils.Array.GetRandom(enemyCells);
      Phaser.Utils.Array.Remove(enemyCells, enemyCell);
      const enemy = this.physics.add.sprite(
        enemyCell.x * tileSize + tileSize / 2,
        enemyCell.y * tileSize + tileSize / 2,
        "enemy"
      );
      enemy.setDisplaySize(tileSize * 0.8, tileSize * 0.8);
      enemy.setCollideWorldBounds(true);
      enemy.setPipeline("Light2D");
      this.physics.add.collider(enemy, this.wallsGroup);
      enemy.redOutline = this.add.graphics();
      enemy.redOutline.lineStyle(2, 0xff0000, 1);
      enemy.redOutline.strokeRect(
        enemy.x - enemy.displayWidth / 2,
        enemy.y - enemy.displayHeight / 2,
        enemy.displayWidth,
        enemy.displayHeight
      );
      this.physics.add.overlap(this.player, enemy, () => {
        if (!window.inBattle) {
          this.startBattle(enemy);
        }
      });
      this.enemies.push(enemy);
    }

    this.keys = this.input.keyboard.addKeys("W,S,A,D,SHIFT,E");
    this.cameras.main.startFollow(this.player);
    this.lightRadius = 150;
    this.playerLight = this.lights.addLight(this.player.x, this.player.y, this.lightRadius, 0xffffff, 1);
    document.getElementById("hud").style.display = "block";
    document.getElementById("game-controls").style.display = "block";

    const startGameMusic = document.getElementById("start-game-sound");
    const bgMusic = document.getElementById("background-music");
    fadeAudio(startGameMusic, 0, 1000, () => {
      startGameMusic.pause();
      startGameMusic.currentTime = 0;
      bgMusic.volume = 0;
      bgMusic.play();
      fadeAudio(bgMusic, 1, 1000);
    });

    this.playerMaxHealth = 10;
    this.playerHealth = 10;
    this.playerMaxMana = 5;
    this.playerMana = 5;
    window.inBattle = false;
    window.currentTurn = "none";
    updateHealthBar(this.playerHealth, this.playerMaxHealth);
    updateManaBar(this.playerMana, this.playerMaxMana);
    updateLevelText();
    updateScoreText();
  }

  update() {
    if (!window.isGameActive) return;
    this.handleMovement();
    if (this.playerLight) {
      this.playerLight.setPosition(this.player.x, this.player.y);
    }
    const vicinityThreshold = 200;
    this.enemies.forEach(enemy => {
      const distance = Phaser.Math.Distance.Between(enemy.x, enemy.y, this.player.x, this.player.y);
      if (distance < vicinityThreshold) {
        enemy.redOutline.clear();
        enemy.redOutline.lineStyle(2, 0xff0000, 1);
        enemy.redOutline.strokeRect(
          enemy.x - enemy.displayWidth / 2,
          enemy.y - enemy.displayHeight / 2,
          enemy.displayWidth,
          enemy.displayHeight
        );
      } else {
        enemy.redOutline.clear();
      }
    });
    if (!this.levelCompleted && this.enemies.length === 0 && !window.inBattle) {
      this.levelCompleted = true;
      this.nextLevel();
    }
  }

  handleMovement() {
    if (window.inBattle) {
      this.player.setVelocity(0);
      return;
    }
    const speed = this.keys.SHIFT.isDown ? 200 : 120;
    let vx = 0, vy = 0;
    if (this.keys.W.isDown) vy = -speed;
    else if (this.keys.S.isDown) vy = speed;
    if (this.keys.A.isDown) vx = -speed;
    else if (this.keys.D.isDown) vx = speed;
    this.player.setVelocity(vx, vy);
  }

  startBattle(enemySprite) {
    window.inBattle = true;
    window.currentTurn = "player";
    this.currentEnemy = enemySprite;
    this.enemyMaxHealth = 5;
    this.enemyHealth = 5;
    showBattleUI(true);
    document.getElementById("enemy-health-bar").style.display = "block";
    updateEnemyHealthBar(this.enemyHealth, this.enemyMaxHealth);
  }

  nextLevel() {
    window.currentLevel++;
    this.playerHealth = this.playerMaxHealth;
    this.playerMana = this.playerMaxMana;
    updateHealthBar(this.playerHealth, this.playerMaxHealth);
    updateManaBar(this.playerMana, this.playerMaxMana);
    updateLevelText();
    this.time.delayedCall(1000, () => {
      this.scene.restart();
    });
  }
}
'''}))
        print("Crew 3 done", result.raw)
        self.state.crew3_output = result.raw   

def kickoff():
    print("Starting kickoff()")
    crews_flow = CrewsFlow()
    crews_flow.kickoff()
    print("Crew1 output:", crews_flow.state.crew1_output)
    print("Crew2 output:", crews_flow.state.crew2_output)

def plot():
    crews_flow = CrewsFlow()
    crews_flow.plot()

if __name__ == "__main__":
    kickoff()
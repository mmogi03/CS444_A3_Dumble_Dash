#!/usr/bin/env python
import warnings
from datetime import datetime
import sys
from pathlib import Path

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
        result = (
            Crew3().crew().kickoff(inputs = {"crew1_output": self.state.crew1_output , "crew2_output": self.state.crew2_output, 
                                   "template": '''
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
                                </html> ''' }))
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
// main.js

// Import necessary modules and classes
// Assuming all classes and functions are available in the same directory or properly exported from their respective files
import { SceneManager, ForgottenCryptScene } from './scenes';
import { GameUI } from './ui';
import { AudioManager } from './audio';
import { Renderer } from './renderer';

// Initialize the game components
const sceneManager = new SceneManager();
const gameUI = new GameUI();

// Set up the initial scene
sceneManager.changeScene(new ForgottenCryptScene());

// Function to start the game
function startGame() {
    document.getElementById('main-menu').classList.add('hidden');
    document.getElementById('game-hud').classList.remove('hidden');
    AudioManager.playBackgroundMusic('exploration'); // Play exploration music when the game starts
    gameLoop(); // Start the game loop
}

// Game loop
function gameLoop() {
    sceneManager.update();
    sceneManager.render();
    requestAnimationFrame(gameLoop);
}

// Event listeners for UI buttons
document.querySelector('button[onclick="startGame()"]').addEventListener('click', startGame);
document.querySelector('button[onclick="showSettings()"]').addEventListener('click', showSettings);
document.querySelector('button[onclick="showCredits()"]').addEventListener('click', showCredits);
document.querySelector('button[onclick="endTurn()"]').addEventListener('click', endTurn);

// Initialize the game
startGame();
// src/main.js // Entry point: sets up the Phaser game, imports scenes & utilities, and manages DOM events
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
window.game = game; 
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

  gameRestartButton.addEventListener("click", () => {
    showScreen(gameScreen);
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
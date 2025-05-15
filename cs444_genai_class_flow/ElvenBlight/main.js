// src/main.js

import BootScene from "./src/scenes/BootScene.js";
import BossScene from "./src/scenes/BossScene.js";
import OverworldScene from "./src/scenes/OverworldScene.js";
import { fadeAudio, setGlobalVolume } from "./src/utils/audio.js";
import {
  updateHealthBar,
  updateManaBar,
  updateLevelText,
  updateScoreText,
} from "./src/utils/ui.js";
import { castSpell, doEnemyTurn } from "./src/utils/battle.js";

// Global game state
window.isGameActive = false;
window.currentDifficulty = "easy";
window.currentTurn = "none";
window.playerPoints = 0;
window.score = 0;

const config = {
  type: Phaser.AUTO,
  parent: "game-container",
  width: window.innerWidth,
  height: window.innerHeight - 64,
  scale: {
    mode: Phaser.Scale.RESIZE,
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
  physics: {
    default: "arcade",
    arcade: { debug: false },
  },
  scene: [],
};

const game = new Phaser.Game(config);
window.game = game;
game.scene.add("BootScene", BootScene);
game.scene.add("OverworldScene", OverworldScene);
game.scene.add("BossScene", BossScene);

document.addEventListener("DOMContentLoaded", () => {
  const startGameMusic = document.getElementById("start-game-sound");
  const bgMusic = document.getElementById("background-music");
  const endGameMusic = document.getElementById("end-game-music");

  // Volume slider hookup
  const volumeSlider = document.getElementById("volume-slider");
  setGlobalVolume(volumeSlider.value);
  volumeSlider.addEventListener("input", (e) => {
    setGlobalVolume(e.target.value);
  });

  // ensure menu music plays, fall back on user interaction if blocked
  if (startGameMusic) {
    const playPromise = startGameMusic.play();
    if (playPromise !== undefined && playPromise.catch) {
      playPromise.catch(() => {
        const resumeAudio = () => {
          startGameMusic.play();
          document.removeEventListener('click', resumeAudio);
        };
        document.addEventListener('click', resumeAudio);
      });
    }
  }

  // Difficulty radios
  const difficultyRadios = document.querySelectorAll(
    'input[name="difficulty"]'
  );
  // on load, check the one matching currentDifficulty
  difficultyRadios.forEach((radio) => {
    if (radio.value === window.currentDifficulty) {
      radio.checked = true;
    }
    radio.addEventListener("change", (e) => {
      window.currentDifficulty = e.target.value;
    });
  });

  // Screen elements
  const startMenuScreen = document.getElementById("start-menu-screen");
  const settingsScreen = document.getElementById("settings-screen");
  const instructionsScreen = document.getElementById("instructions-screen");
  const gameScreen = document.getElementById("game-screen");
  const gameOverScreen = document.getElementById("game-over-screen");
  const hud = document.getElementById("hud");
  const gameControls = document.getElementById("game-controls");

  // Buttons
  const playButton = document.getElementById("play-button");
  const settingsButton = document.getElementById("settings-button");
  const instructionsButton = document.getElementById("instructions-button");
  const settingsBackButton = document.getElementById("settings-back-button");
  const instructionsBackButton = document.getElementById(
    "instructions-back-button"
  );
  const gameMenuButton = document.getElementById("game-menu-button");
  const gameRestartButton = document.getElementById("game-restart-button");
  const gameInstructionsButton = document.getElementById(
    "game-instructions-button"
  );
  const playAgainButton = document.getElementById("play-again-button");
  const mainMenuButton = document.getElementById("main-menu-button");

  // Spell cards
  const fireballCard = document.getElementById("fireball-card");
  const mudwallCard = document.getElementById("mudwall-card");
  const healCard = document.getElementById("heal-card");
  const skipTurnButton = document.getElementById("skip-turn-button");

  // Helper: stop any end‑game music
  function stopEndGameMusic() {
    if (endGameMusic) {
      endGameMusic.pause();
      endGameMusic.currentTime = 0;
    }
  }

  // Show exactly one screen, hide the rest
  function showScreen(screen) {
    stopEndGameMusic();
    [
      startMenuScreen,
      settingsScreen,
      instructionsScreen,
      gameScreen,
      gameOverScreen,
    ].forEach((s) => s.classList.remove("active"));
    if (screen) screen.classList.add("active");
  }

  // Play button: start or resume
  playButton.addEventListener("click", () => {
    stopEndGameMusic();
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

  // Navigation buttons
  settingsButton.addEventListener("click", () => showScreen(settingsScreen));
  instructionsButton.addEventListener("click", () =>
    showScreen(instructionsScreen)
  );

  settingsBackButton.addEventListener("click", () => {
    stopEndGameMusic();
    // if game is paused (pause menu), always return to main menu
    if (game.scene.isPaused("OverworldScene") && window.isGameActive) {
      showScreen(startMenuScreen);
    } else if (window.isGameActive) {
      // return to active game
      showScreen(gameScreen);
      if (game.scene.isPaused("OverworldScene")) {
        game.scene.resume("OverworldScene");
      }
    } else {
      // not in game, go to main menu
      showScreen(startMenuScreen);
    }
  });
  instructionsBackButton.addEventListener("click", () => {
    stopEndGameMusic();
    // if game is paused (pause menu), always return to main menu
    if (game.scene.isPaused("OverworldScene") && window.isGameActive) {
      showScreen(startMenuScreen);
    } else if (window.isGameActive) {
      // return to active game
      showScreen(gameScreen);
      if (game.scene.isPaused("OverworldScene")) {
        game.scene.resume("OverworldScene");
      }
    } else {
      // not in game, go to main menu
      showScreen(startMenuScreen);
    }
  });

  gameMenuButton.addEventListener("click", () => {
    stopEndGameMusic();
    showScreen(startMenuScreen);
    game.scene.pause("OverworldScene");
  });

  gameRestartButton.addEventListener("click", () => {
    stopEndGameMusic();
    showScreen(gameScreen);
    const battleUI = document.getElementById("battle-ui");
    if (battleUI) battleUI.style.display = "none";
    window.isGameActive = true;
    game.scene.start("OverworldScene");
  });

  gameInstructionsButton.addEventListener("click", () =>
    showScreen(instructionsScreen)
  );

  // End‑game screen buttons
  playAgainButton.addEventListener("click", () => {
    window.location.href = window.location.pathname + "?autoStart=true";
  });
  mainMenuButton.addEventListener("click", () => {
    window.location.reload();
  });

  // Bind spell card clicks
  fireballCard.addEventListener("click", () => castSpell("fireball"));
  mudwallCard.addEventListener("click", () => castSpell("mudWall"));
  healCard.addEventListener("click", () => castSpell("astralHeal"));
  skipTurnButton.addEventListener("click", () => {
    window.currentTurn = "enemy";
    doEnemyTurn();
  });

  // Auto‑start logic
  const params = new URLSearchParams(window.location.search);
  if (params.get("autoStart") === "true") {
    playButton.click();
  }
});

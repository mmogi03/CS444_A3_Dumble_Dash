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
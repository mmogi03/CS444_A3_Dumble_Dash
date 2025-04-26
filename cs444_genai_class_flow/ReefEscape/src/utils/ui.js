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
  
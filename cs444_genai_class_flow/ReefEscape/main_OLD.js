// Global variables
window.isGameActive = false;
window.currentDifficulty = 'easy';
window.currentTurn = 'none';
window.playerPoints = 0;
window.score = 0;

function setGlobalVolume(vol) {
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

function fadeAudio(audio, targetVolume, duration, callback) {
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

const SpellCosts = {
  fireball: 3,
  mudWall: 1,
  astralHeal: 3
};

function updateHealthBar(current, max) {
  const pct = (current / max) * 100;
  document.getElementById("health-fill").style.width = pct + "%";
}

function updateManaBar(current, max) {
  const pct = (current / max) * 100;
  document.getElementById("mana-fill").style.width = pct + "%";
}

function updateEnemyHealthBar(current, max) {
  const pct = (current / max) * 100;
  document.getElementById("enemy-health-fill").style.width = pct + "%";
}

function showBattleUI(flag) {
  const battleUI = document.getElementById("battle-ui");
  if (battleUI) {
    battleUI.style.display = flag ? "flex" : "none";
  }
}

function updateLevelText() {
  document.getElementById("level-text").innerText = "Level: " + window.currentLevel;
}

function updateScoreText() {
  document.getElementById("score-text").innerText = "Score: " + window.score;
}

class BootScene extends Phaser.Scene {
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

class OverworldScene extends Phaser.Scene {
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
    let columns = Math.floor(gameWidth / baseTileSize);
    let rows = Math.round(columns * (gameHeight / gameWidth));
    let tileSize = Math.min(gameWidth / columns, gameHeight / rows);
    this.lights.enable();
    this.lights.setAmbientColor(0x000000);
    const maze = generateMaze(columns, rows);
    this.groundGroup = this.add.group();
    this.wallsGroup = this.physics.add.staticGroup();
    for (let y = 0; y < rows; y++) {
      for (let x = 0; x < columns; x++) {
        const worldX = x * tileSize;
        const worldY = y * tileSize;
        let groundTile = this.groundGroup.create(worldX + tileSize / 2, worldY + tileSize / 2, "ground");
        groundTile.setDisplaySize(tileSize, tileSize);
        groundTile.setPipeline('Light2D');
        if (maze[y][x] === 1) {
          let wallTile = this.wallsGroup.create(worldX + tileSize / 2, worldY + tileSize / 2, "wall");
          wallTile.setDisplaySize(tileSize, tileSize);
          wallTile.refreshBody();
          wallTile.setPipeline('Light2D');
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
    this.player.setPipeline('Light2D');
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
      enemy.setPipeline('Light2D');
      this.physics.add.collider(enemy, this.wallsGroup);
      enemy.redOutline = this.add.graphics();
      enemy.redOutline.lineStyle(2, 0xFF0000, 1);
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
        enemy.redOutline.lineStyle(2, 0xFF0000, 1);
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

function generateMaze(width, height) {
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

function getOpenCells(maze) {
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

  // Updated Play Button: resume if game is active; else start new game
  playButton.addEventListener("click", () => {
    if (window.isGameActive) {
      showScreen(gameScreen);
      // Resume the paused scene if necessary
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

  // Updated Back buttons: if game is active, return to game; otherwise go to main menu
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

  // Updated Main Menu Button on Game Over (okay to return to main menu)
  mainMenuButton.addEventListener("click", () => {
    showScreen(startMenuScreen);
    window.isGameActive = false;
  });

  // Updated Menu Button: pause the scene but leave window.isGameActive true so it can be resumed
  gameMenuButton.addEventListener("click", () => {
    showScreen(startMenuScreen);
    game.scene.pause("OverworldScene");
  });

  // Restart button continues to restart the game as before
  gameRestartButton.addEventListener("click", () => {
    showScreen(gameScreen);
    window.isGameActive = true;
    game.scene.start("OverworldScene");
  });

  // In-game Instructions Button: simply show the instructions screen
  gameInstructionsButton.addEventListener("click", () => {
    showScreen(instructionsScreen);
  });

  const battleUI = document.getElementById("battle-ui");
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

  // Modified castSpell: hide battleUI immediately before enemy tint begins.
  function castSpell(spellName) {
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

  // Modified enemy turn function: player's red overlay appears after a 500ms delay,
  // then a longer pause (1 second) before applying enemy damage and re-showing battleUI.
  function doEnemyTurn() {
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
      // Extended pause after the player's red overlay before processing enemy damage
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

  function endBattle(scene, playerWon) {
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

  function showGameOver() {
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

  function getCurrentScene() {
    if (game.scene.isActive("OverworldScene")) return game.scene.getScene("OverworldScene");
    return null;
  }
});

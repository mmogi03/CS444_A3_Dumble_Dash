// src/scenes/OverworldScene.js
import { fadeAudio } from "../utils/audio.js";
import {
  updateHealthBar,
  updateManaBar,
  updateLevelText,
  updateScoreText,
  updateEnemyHealthBar,
  showBattleUI,
} from "../utils/ui.js";
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

        const groundTile = this.groundGroup.create(
          worldX + tileSize / 2,
          worldY + tileSize / 2,
          "ground"
        );
        groundTile.setDisplaySize(tileSize, tileSize);
        groundTile.setPipeline("Light2D");

        if (maze[y][x] === 1) {
          const wallTile = this.wallsGroup.create(
            worldX + tileSize / 2,
            worldY + tileSize / 2,
            "wall"
          );
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
    const enemyCells = openCells.filter(
      (cell) => !(cell.x === playerCell.x && cell.y === playerCell.y)
    );
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
    this.playerLight = this.lights.addLight(
      this.player.x,
      this.player.y,
      this.lightRadius,
      0xffffff,
      1
    );

    document.getElementById("hud").style.display = "block";
    document.getElementById("game-controls").style.display = "block";

    // AUDIO HANDLING
    const startGameMusic = document.getElementById("start-game-sound");
    const bgMusic = document.getElementById("background-music");
    const volumeSlider = document.getElementById("volume-slider");
    const targetVol = parseFloat(volumeSlider.value);

    fadeAudio(startGameMusic, 0, 1000, () => {
      startGameMusic.pause();
      startGameMusic.currentTime = 0;

      bgMusic.volume = 0;
      bgMusic.play().catch(() => {});

      bgMusic.addEventListener("timeupdate", () => {
        if (bgMusic.currentTime >= bgMusic.duration - 2) {
          bgMusic.currentTime = 0;
        }
      });

      fadeAudio(bgMusic, targetVol, 1000);
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
    this.enemies.forEach((enemy) => {
      const distance = Phaser.Math.Distance.Between(
        enemy.x,
        enemy.y,
        this.player.x,
        this.player.y
      );
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
    let vx = 0,
      vy = 0;
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

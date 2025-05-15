// src/scenes/BootScene.js
export default class BootScene extends Phaser.Scene {
  constructor() {
    super("BootScene");
  }

  preload() {
    // main character
    this.load.image("player", "images/main_character.png");
    // boss/enemy sprite
    this.load.image("enemy", "images/enemy.png");
    // (we still keep the castle if you use it elsewhere)
    //this.load.image("castle", "images/castle.png");
    // dungeon floor → grass tiles
    this.load.image("ground", "images/grass_tile.png");
    // brick wall → elven wall
    this.load.image("wall", "images/elven_wall.png");
    // boss background for rhythm game
    this.load.image("bossBackground", "images/boss_background.png");
    // boss scene audio
    this.load.audio("bossMusic", "sounds/boss_music.ogg");
    this.load.audio("enemyAttack", "sounds/enemy_attack_sound.ogg");
    this.load.audio("victorySnd", "sounds/level_victory_sound.ogg");
  }

  create() {
    // reset boss sequence flag and start overworld
    window.justFinishedBoss = false;
    this.scene.start("OverworldScene");
  }
}

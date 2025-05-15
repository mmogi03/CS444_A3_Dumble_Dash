// src/scenes/BootScene.js
export default class BootScene extends Phaser.Scene {
  constructor() {
    super("BootScene");
  }

  preload() {
    // main character
    this.load.image("player", "assets/textures/main_character.png");
    // boss/enemy sprite
    this.load.image("enemy", "assets/textures/enemy.png");
    // (we still keep the castle if you use it elsewhere)
    //this.load.image("castle", "assets/castle.png");
    // dungeon floor → grass tiles
    this.load.image("ground", "assets/textures/grass_tile.png");
    // brick wall → elven wall
    this.load.image("wall", "assets/textures/elven_wall.png");
    // boss background for rhythm game
    this.load.image("bossBackground", "assets/textures/boss_background.png");
  }

  create() {
    // reset boss sequence flag and start overworld
    window.justFinishedBoss = false;
    this.scene.start("OverworldScene");
  }
}

// src/scenes/BootScene.js
export default class BootScene extends Phaser.Scene {
  constructor() {
    super("BootScene");
  }

  preload() {
    // main character
    this.load.image("player", "assets/textures/main_character.webp");
    // boss/enemy sprite
    this.load.image("enemy", "assets/textures/boss_1.webp");
    // (we still keep the castle if you use it elsewhere)
    this.load.image("castle", "assets/castle.png");
    // dungeon floor → water tiles
    this.load.image("ground", "assets/textures/water_tile.png");
    // brick wall → coral wall
    this.load.image("wall", "assets/textures/coral_wall.png");
  }

  create() {
    this.scene.start("OverworldScene");
  }
}

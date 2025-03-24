export default class BootScene extends Phaser.Scene {
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
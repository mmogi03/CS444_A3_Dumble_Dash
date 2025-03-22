// game.js
// Simple Phaser 3 scene with code-generated circle sprite controlled by WASD

var config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    parent: 'game-container',  // The DOM element id where the game is injected
    physics: {
        default: 'arcade',
        arcade: {
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

var player;
var cursors;

var gameInstance = new Phaser.Game(config);

function preload() {
    // We don't need to load any external images
    // We'll draw the player using Phaser's graphics
}

function create() {
    // Create a graphics object to draw a circle for our player
    var graphics = this.add.graphics({ fillStyle: { color: 0xffffff } });
    // Draw the circle (x, y, radius)
    graphics.fillCircle(0, 0, 20);

    // Render texture from the graphics
    var textureKey = 'player_circle';
    graphics.generateTexture(textureKey, 40, 40); // 2*radius in each dimension

    // Create sprite from that texture
    player = this.physics.add.sprite(400, 300, textureKey);

    // Register keyboard cursors (WASD or Arrow keys)
    cursors = this.input.keyboard.addKeys({
      up: Phaser.Input.Keyboard.KeyCodes.W,
      down: Phaser.Input.Keyboard.KeyCodes.S,
      left: Phaser.Input.Keyboard.KeyCodes.A,
      right: Phaser.Input.Keyboard.KeyCodes.D
    });
}

function update() {
    // Movement speed
    var speed = 200;

    // Reset velocity
    player.setVelocity(0);

    if (cursors.left.isDown) {
        player.setVelocityX(-speed);
    }
    else if (cursors.right.isDown) {
        player.setVelocityX(speed);
    }

    if (cursors.up.isDown) {
        player.setVelocityY(-speed);
    }
    else if (cursors.down.isDown) {
        player.setVelocityY(speed);
    }
}

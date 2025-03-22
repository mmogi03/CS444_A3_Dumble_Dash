// game.js
// Generalized Phaser 3 template with placeholders to fill in.

var config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    parent: 'game-container',  // Must match index.html
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

var gameInstance = new Phaser.Game(config);

var player;

function preload() {
    // Placeholder for preload code
    // No assets to preload for a simple circle
}

function create() {
    // Create the player as a simple circle
    player = this.physics.add.circle(400, 300, 20, 0xffff00); // Yellow circle with radius 20
    player.setCollideWorldBounds(true); // Prevent the player from going out of bounds

    // Enable keyboard inputs
    this.cursors = this.input.keyboard.createCursorKeys();
    this.wasdKeys = {
        W: this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.W),
        A: this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.A),
        S: this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.S),
        D: this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.D)
    };
}

function update() {
    // Movement logic
    player.setVelocity(0); // Reset velocity

    if (this.wasdKeys.W.isDown) {
        player.setVelocityY(-150); // Move up
    } else if (this.wasdKeys.S.isDown) {
        player.setVelocityY(150); // Move down
    }

    if (this.wasdKeys.A.isDown) {
        player.setVelocityX(-150); // Move left
    } else if (this.wasdKeys.D.isDown) {
        player.setVelocityX(150); // Move right
    }
}


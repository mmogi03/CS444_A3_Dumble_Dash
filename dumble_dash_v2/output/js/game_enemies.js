// game_enemies.js

function spawnEnemy(scene) {
    // Generate a random position within the bounds of the game
    const x = Phaser.Math.Between(0, scene.cameras.main.width);
    const y = Phaser.Math.Between(0, scene.cameras.main.height);

    // Create a graphics object for the enemy
    const enemy = scene.add.graphics({ fillStyle: { color: 0xff0000 } }); // Red color
    const shapeType = Phaser.Math.Between(1, 2); // 1 for square, 2 for triangle

    // Draw the shape based on random type
    if (shapeType === 1) {
        enemy.fillRect(x, y, 20, 20); // Square
    } else {
        enemy.fillTriangle(x, y, x + 20, y + 20, x - 20, y + 20); // Triangle
    }

    // Enable physics for the enemy
    scene.physics.add.existing(enemy);
    enemy.body.setVelocity(Phaser.Math.Between(-50, 50), Phaser.Math.Between(-50, 50));
    enemy.body.setCollideWorldBounds(true);
    enemy.body.setBounce(1); // Makes it bounce off walls
}

function startEnemySpawn(scene) {
    // Spawn an enemy every 2 seconds
    scene.time.addEvent({
        delay: 2000,
        callback: () => spawnEnemy(scene),
        loop: true
    });
}

// Assuming this part is inside the create function of your Phaser scene
startEnemySpawn(this);

function updateEnemies() {
    // Update function for enemies if needed
}

// Add the update function to the existing update method in game.js
// Call updateEnemies() if you want to add additional logic for the enemies later
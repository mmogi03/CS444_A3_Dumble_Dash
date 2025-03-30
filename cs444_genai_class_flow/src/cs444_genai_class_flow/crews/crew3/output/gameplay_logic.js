class Card {
    constructor(name, cost, effect) {
        this.name = name;
        this.cost = cost;
        this.effect = effect;
    }

    play(target, player) {
        if (player.energy >= this.cost) {
            player.energy -= this.cost;
            this.effect(target, player);
        }
    }
}

class Player {
    constructor(name, health, energy) {
        this.name = name;
        this.health = health;
        this.energy = energy;
        this.deck = [];
        this.hand = [];
    }

    drawCard() {
        if (this.deck.length > 0) {
            this.hand.push(this.deck.pop());
        }
    }

    startTurn() {
        this.energy = 3; // Reset energy at the start of each turn
        this.drawCard();
    }
}

class Enemy {
    constructor(name, health) {
        this.name = name;
        this.health = health;
    }

    takeTurn(player) {
        // Simple enemy action for demonstration
        player.health -= 1;
    }
}

class Game {
    constructor(player, enemy) {
        this.player = player;
        this.enemy = enemy;
        this.turn = 0;
    }

    nextTurn() {
        this.turn++;
        if (this.turn % 2 === 1) {
            this.player.startTurn();
        } else {
            this.enemy.takeTurn(this.player);
        }
    }

    playCard(cardIndex, target) {
        const card = this.player.hand[cardIndex];
        if (card) {
            card.play(target, this.player);
            this.player.hand.splice(cardIndex, 1);
        }
    }
}

// Example usage
const fireball = new Card('Fireball', 2, (target, player) => {
    target.health -= 3;
});

const player = new Player('Hero', 10, 3);
const enemy = new Enemy('Goblin', 5);

player.deck.push(fireball);
player.drawCard();

const game = new Game(player, enemy);

// Simulate a full combat round
game.nextTurn(); // Player's turn
game.playCard(0, enemy); // Player plays Fireball
game.nextTurn(); // Enemy's turn

console.log(`Player Health: ${player.health}, Enemy Health: ${enemy.health}`);
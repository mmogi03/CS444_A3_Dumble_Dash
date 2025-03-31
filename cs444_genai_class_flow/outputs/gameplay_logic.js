Here is a modular JavaScript implementation for turn-based card combat in "Shadowreapers: The Eclipse Chronicles." This code includes classes for Card, Deck, Player, Enemy, and the Game, demonstrating the combat round with energy management and level interactions.

```javascript
class Card {
    constructor(name, cost, effect) {
        this.name = name;
        this.cost = cost;
        this.effect = effect;
    }
}

class Deck {
    constructor(cards = []) {
        this.cards = cards;
    }

    draw() {
        return this.cards.pop();
    }

    shuffle() {
        for (let i = this.cards.length -1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i +1));
            [this.cards[i], this.cards[j]] = [this.cards[j], this.cards[i]];
        }
    }
}

class Player {
    constructor(name, deck, maxEnergy = 3) {
        this.name = name;
        this.deck = deck;
        this.hand = [];
        this.maxEnergy = maxEnergy;
        this.currentEnergy = maxEnergy;
        this.health = 30;
        this.position = 0;
    }

    drawHand() {
        for (let i = 0; i < 5; i++) {
            const card = this.deck.draw();
            if (card) this.hand.push(card);
        }
    }

    resetEnergy() {
        this.currentEnergy = this.maxEnergy;
    }

    playCard(cardIndex, target, opponent) {
        const card = this.hand[cardIndex];
        if (card && card.cost <= this.currentEnergy) {
            this.currentEnergy -= card.cost;
            card.effect(this, target, opponent);
            this.hand.splice(cardIndex, 1);
        }
    }
}

class Enemy {
    constructor(name, health, behavior) {
        this.name = name;
        this.health = health;
        this.behavior = behavior;
        this.position = 5;
    }

    takeTurn(player, enemies) {
        this.behavior(this, player, enemies);
    }
}

class Game {
    constructor(player, enemies) {
        this.player = player;
        this.enemies = enemies;
        this.turn = 'player';
    }

    startCombat() {
        this.player.deck.shuffle();
        this.player.drawHand();
        this.gameLoop();
    }

    gameLoop() {
        while(this.player.health > 0 && this.enemies.some(e => e.health > 0)) {
            if(this.turn === 'player') {
                this.player.resetEnergy();
                // Example: Player plays the first card targeting the first enemy
                this.player.playCard(0, this.enemies[0], this.enemies[0]);
                this.turn = 'enemy';
            } else {
                this.enemies.forEach(enemy => {
                    if(enemy.health > 0) {
                        enemy.takeTurn(this.player, this.enemies);
                    }
                });
                this.turn = 'player';
                this.player.drawHand();
            }
        }
        if(this.player.health <=0 ){
            console.log('Player defeated!');
        } else {
            console.log('Enemies defeated!');
        }
    }
}

// Example card effects
function attackEffect(user, target, opponent) {
    target.health -= 5;
}

function healEffect(user, target, opponent) {
    user.health += 3;
}

// Creating cards
const attackCard = new Card('Strike', 1, attackEffect);
const healCard = new Card('Heal', 2, healEffect);

// Creating decks
const playerDeck = new Deck([attackCard, attackCard, healCard, attackCard, attackCard]);

// Creating player and enemy
const player = new Player('Hero', playerDeck);
const enemy = new Enemy('Goblin', 15, (enemy, player, enemies) => {
    player.health -= 2; // Enemy attacks
});

// Starting the game
const game = new Game(player, [enemy]);
game.startCombat();
```

This example simulates a full combat round where the player and enemy take turns. Players can draw cards, manage their energy, and make strategic decisions based on their deck and available actions. The modularity ensures easy addition of new cards and mechanics.
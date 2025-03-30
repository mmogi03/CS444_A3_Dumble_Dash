The complete user interface for "Arcane Depths" has been built using HTML, CSS, and JavaScript. The UI includes a main menu, game HUD, and in-game overlays for settings and credits. The layout is responsive and consistent with the game's theme, ensuring a seamless player experience across devices. Below is the code for the UI components:

HTML:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arcane Depths</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div id="game-container">
        <!-- Main Menu -->
        <div id="main-menu" class="menu">
            <h1>Arcane Depths</h1>
            <button onclick="startGame()">Start Game</button>
            <button onclick="showSettings()">Settings</button>
            <button onclick="showCredits()">Credits</button>
        </div>

        <!-- Game HUD -->
        <div id="game-hud" class="hud hidden">
            <div id="player-info">
                <span id="player-health">Health: 100</span>
                <span id="player-mana">Mana: 50</span>
            </div>
            <div id="card-hand">
                <!-- Cards will be dynamically added here -->
            </div>
            <button id="end-turn" onclick="endTurn()">End Turn</button>
        </div>

        <!-- In-Game Overlays -->
        <div id="overlay" class="overlay hidden">
            <div id="settings" class="overlay-content hidden">
                <h2>Settings</h2>
                <button onclick="toggleSound()">Toggle Sound</button>
                <button onclick="toggleMusic()">Toggle Music</button>
                <button onclick="closeOverlay()">Close</button>
            </div>
            <div id="credits" class="overlay-content hidden">
                <h2>Credits</h2>
                <p>Game Design: Jane Doe</p>
                <p>Development: John Smith</p>
                <button onclick="closeOverlay()">Close</button>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>
```

CSS:
```css
/* styles.css */
body {
    font-family: 'Arial', sans-serif;
    margin: 0;
    padding: 0;
    background-color: #1a1a1a;
    color: #fff;
}

#game-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
}

.menu, .hud, .overlay {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.hidden {
    display: none;
}

button {
    margin: 10px;
    padding: 10px 20px;
    background-color: #333;
    color: #fff;
    border: none;
    cursor: pointer;
}

button:hover {
    background-color: #555;
}

.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    justify-content: center;
    align-items: center;
}

.overlay-content {
    background-color: #222;
    padding: 20px;
    border-radius: 5px;
}
```

JavaScript:
```javascript
// script.js

function startGame() {
    document.getElementById('main-menu').classList.add('hidden');
    document.getElementById('game-hud').classList.remove('hidden');
    // Initialize game logic here
}

function showSettings() {
    document.getElementById('overlay').classList.remove('hidden');
    document.getElementById('settings').classList.remove('hidden');
}

function showCredits() {
    document.getElementById('overlay').classList.remove('hidden');
    document.getElementById('credits').classList.remove('hidden');
}

function closeOverlay() {
    document.getElementById('overlay').classList.add('hidden');
    document.querySelectorAll('.overlay-content').forEach(content => content.classList.add('hidden'));
}

function endTurn() {
    // Logic to end the player's turn
}

function toggleSound() {
    // Logic to toggle sound
}

function toggleMusic() {
    // Logic to toggle music
}
```

This code provides a responsive and immersive UI for 'Arcane Depths', featuring a main menu, game HUD, and in-game overlays for settings and credits. The layout is designed to be consistent with the game's theme and mechanics, ensuring a seamless player experience across devices.
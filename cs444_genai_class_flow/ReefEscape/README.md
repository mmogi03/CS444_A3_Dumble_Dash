# 🌊 Reef Escape

**Reef Escape** is a 2D infinite crawler and spiritual successor to *DumbleDash*. You play as **Nerida**, a young mermaid separated from her family, trying to escape the mystical but dangerous Reef. As you swim deeper into the ocean, you must evade deadly terrain, fight off hostile reef mermaids, and uncover the secrets that lie in the deep.

Your goal: survive as long as possible in classic roguelike fashion, while progressing through increasingly difficult levels to reunite Nerida with her lost kin.

---

## 🕹️ How to Run the Game in Your Browser

This game runs in a web browser, but you **cannot** open `index.html` directly by double-clicking it. Modern browsers block local file access for security reasons.

To run *Reef Escape* correctly, you'll need to serve the game using a local development server. Here are a few easy options:

### ✅ Option 1: Use `http-server` with `npx` (No install required)

1. Open your terminal or command prompt.
2. Navigate to the root folder of the game:
   ```
   cd ReefEscape
   ```
3. Run this command:
   ```
   npx http-server
   ```
4. You’ll see a local URL like `http://127.0.0.1:8080`.  
   Open it in your browser to play the game.

If you don’t have `npx`, you can install it by installing [Node.js](https://nodejs.org/), which includes `npx` by default.

---

### ✅ Option 2: Use Live Server in Visual Studio Code

1. Open the `ReefEscape` folder in [Visual Studio Code](https://code.visualstudio.com/).
2. Install the **Live Server** extension:
   - Go to the Extensions tab (or press `Ctrl+Shift+X`)
   - Search for **Live Server**
   - Click **Install**
3. Right-click on `index.html` in the file explorer.
4. Click **"Open with Live Server"**.
5. Your default browser will open and load the game automatically using a local server (usually at `http://127.0.0.1:5500`).

---

### ✅ Option 3: Use Live Share with Go Live (for Collaboration or Demos)

1. Install the following extensions in Visual Studio Code:
   - **Live Share**
   - **Live Server**
2. Start a **Live Share** session.
3. Within the shared session, right-click `index.html` and choose **"Open with Live Server"**.
4. Share the session link with others — they’ll be able to view and play the game in their own browsers using your live server.

---

## 📁 Project Structure

```
ReefEscape/
├── README.md                        # Game documentation and instructions
├── assets/                          # Game assets (audio, music, textures)
│   ├── audio/                       # Sound effects (e.g., tail whip, healing, enemy attacks)
│   │   ├── coral_heal.wav
│   │   ├── enemy_attack_1.mp3
│   │   ├── tail_whip.wav
│   │   └── tidal_splash.wav
│   ├── music/                       # Background music and event cues
│   │   ├── 466133__humanoide9000__victory-fanfare.wav
│   │   ├── background_music_1.wav
│   │   ├── end_game_music.wav
│   │   ├── end_game_music_OLD.mp3
│   │   ├── level_victory.wav
│   │   └── start_game_music.wav
│   ├── textures/                    # In-game visuals (characters, backgrounds, tiles)
│   │   ├── boss_1.webp
│   │   ├── coral_heal.png
│   │   ├── coral_wall.png
│   │   ├── losing_screen.png
│   │   ├── main_character.webp
│   │   ├── main_menu_background.png
│   │   ├── main_menu_background.webp
│   │   ├── tail_whip.png
│   │   ├── tidal_splash.png
│   │   ├── water_tile.jpg
│   │   └── water_tile.png
├── index.html                       # Main entry point for the game
├── main.js                          # Top-level game script
└── src/                             # Core game logic and scene handling
    ├── scenes/                      # Game scenes and flow control
    │   ├── BootScene.js
    │   └── OverworldScene.js
    └── utils/                       # Reusable game utilities and helpers
        ├── audio.js
        ├── battle.js
        ├── maze.js
        └── ui.js
```

---

## ✅ Requirements

- A modern web browser (Chrome, Firefox, Edge, Safari)
- One of the local server options listed above to serve the game files

---

## 🎮 Objective

- Explore an endless underwater world
- Battle evil reef mermaids and survive hostile waters
- Progress through increasingly difficult levels
- Reunite Nerida with her long-lost family

---

💡 Tip: Every time you dive in, the reef changes. No two runs are ever the same.

---

## 🔊 Audio Credits

All sounds used in **Reef Escape** were sourced from [Freesound.org](https://freesound.org/) and are licensed under various Creative Commons licenses:

### 🔹 Creative Commons Attribution 4.0 (CC BY 4.0)
These sounds require attribution. You are free to use, remix, and share them with proper credit.

- **"LittleMermaidsTune.wav"** by [eardeer](https://freesound.org/people/eardeer/) — https://freesound.org/s/387233/
- **"Game Menu/Death Music"** by [ItsRexxys](https://freesound.org/people/ItsRexxys/) — https://freesound.org/s/738242/
- **"ambienta-soundtrack_metaphisical-death.wav"** by [suonho](https://freesound.org/people/suonho/) — https://freesound.org/s/54921/
- **"Monster Roar_10"** by [mitchanary](https://freesound.org/people/mitchanary/) — https://freesound.org/s/505121/
- **"Victory Percussion Music Cue"** by [joshuaempyre](https://freesound.org/people/joshuaempyre/) — https://freesound.org/s/404024/

### 🔹 Creative Commons Attribution 3.0 (CC BY 3.0)
This sound also requires attribution under an earlier version of the license.

- **"Water Splash.wav"** by [Yin_Yang_Jake007](https://freesound.org/people/Yin_Yang_Jake007/) — https://freesound.org/s/406087/

### 🔹 Creative Commons 0 (CC0)
These sounds are in the public domain — no attribution required, but we still gratefully acknowledge the authors:

- **"Sea warriors.wav"** by [szegvari](https://freesound.org/people/szegvari/) — https://freesound.org/s/569367/
- **"Whip02.wav"** by [kingsrow](https://freesound.org/people/kingsrow/) — https://freesound.org/s/348090/
- **"Heal - Rpg"** by [colorsCrimsonTears](https://freesound.org/people/colorsCrimsonTears/) — https://freesound.org/s/562292/
- **"Look out sea - atmo orchestral - sad mood.wav"** by [szegvari](https://freesound.org/people/szegvari/) — https://freesound.org/s/591012/

---

Enjoy the game! 🧜‍♀️💙

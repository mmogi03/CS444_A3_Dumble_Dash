# ✨ Elven Blight

**Elven Blight** is a 2D infinite crawler and spiritual successor to *DumbleDash* & *ReefEscape*. You play as a **brave elf warrior** on a mission to rescue your **captured elf princess**, traversing through the mystical but deadly enchanted forest. With blade and bow, you must fight off twisted woodland creatures, evil elves, and gooey monsters while calling upon the power of nature to survive.

Your goal: survive as long as possible in classic roguelike fashion, while progressing through increasingly dangerous biomes to find and free your princess.

---

## 🕹️ How to Run the Game in Your Browser

This game runs in a web browser, but you **cannot** open `index.html` directly by double-clicking it. Modern browsers block local file access for security reasons.

To run *Elven Blight* correctly, you'll need to serve the game using a local development server. Here are a few easy options:

### ✅ Option 1: Use `http-server` with `npx` (No install required)

1. Open your terminal or command prompt.
2. Navigate to the root folder of the game:

   ```
   cd ElvenBlight
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

1. Open the `ElvenBlight` folder in [Visual Studio Code](https://code.visualstudio.com/).
2. Install the **Live Server** extension:

   * Go to the Extensions tab (or press `Ctrl+Shift+X`)
   * Search for **Live Server**
   * Click **Install**
3. Right-click on `index.html` in the file explorer.
4. Click **"Open with Live Server"**.
5. Your default browser will open and load the game automatically using a local server (usually at `http://127.0.0.1:5500`).

---

### ✅ Option 3: Use Live Share with Go Live (for Collaboration or Demos)

1. Install the following extensions in Visual Studio Code:

   * **Live Share**
   * **Live Server**
2. Start a **Live Share** session.
3. Within the shared session, right-click `index.html` and choose **"Open with Live Server"**.
4. Share the session link with others — they’ll be able to view and play the game in their own browsers using your live server.

---

## 📁 Project Structure

```
ElvenBlight/
├── README.md      
├── index.html       
├── main.js  
├── assets/ 
│   ├── textures/  
├── images/  
    ├── arrow_shot.png
    ├── boss_background.png
    ├── elven_wall.png
    ├── enemy.png
    ├── grass_tile.png
    ├── instructions.png
    ├── losing_screen.png
    ├── main_character.png
    ├── main_menu_background.png
    ├── nature_tree_heal.png
    ├── settings.png
    ├── sword_slash.png
|── sounds/                 
    ├── background_music.mp3
    ├── background_music.ogg
    ├── boss_music.mp3
    ├── boss_music.ogg
    ├── card_attack_sound_1.mp3
    ├── card_attack_sound_1.ogg
    ├── card_attack_sound_2.mp3
    ├── card_attack_sound_2.ogg
    ├── endgame_music.mp3
    ├── endgame_music.ogg
    ├── enemy_attack_sound.mp3
    ├── enemy_attack_sound.ogg
    ├── heal_sound.mp3
    ├── heal_sound.ogg
    ├── level_victory_sound.mp3
    ├── level_victory_sound.ogg
    ├── start_game_sound.mp3
    ├── start_game_sound.ogg
├── src/ 
│   ├── scenes/  
│   │   ├── BootScene.js
│   │   ├── BossScene.js
│   │   └── OverworldScene.js
│   └── utils/ 
│       ├── audio.js
│       ├── battle.js
│       ├── maze.js
│       └── ui.js
```

---

## ✅ Requirements

* A modern web browser (Chrome, Firefox, Edge, Safari)
* One of the local server options listed above to serve the game files

---

## 🎮 Objective

* You are a brave elf on a quest to rescue your captured elf princess!
* Battle through the natural enchanted forests and defeat evil elves and twisted woodland, gooey monsters.
* Use your **Nature Sword Strike** and **Arrow Flurry** to deal damage, while **Forest Blessing** restores your health.
* Survive the dark forest and uncover the mystery of the elven blight!

---

💡 Tip: The forest shifts each time you enter. No two quests are the same.

---

## Target Audience

Our target audience is mostly people who enjoy strategy games, especially fans of turn-based card battlers and roguelikes. We were thinking about players who like games like Slay the Spire or Dicey Dungeons, where planning and decision-making are just as important as action. It's also meant to be accessible for casual gamers since the cartoon style and simple controls make it easy to get into. We wanted it to work well on both desktop and mobile so more people could play it on the go. Overall, it’s for anyone who likes fun, fast-paced battles with a bit of story and challenge mixed in.

## 🔊 Audio Credits

All sounds used in **Elven Blight** were sourced from [Freesound.org](https://freesound.org/) and are licensed under various Creative Commons licenses. Below each entry shows the in-code filename, the original sound title and author, the source URL, and the applicable license:

### 🔹 Creative Commons Attribution 4.0 (CC BY 4.0)

* `level_victory_sound.ogg`  
  **“Charm”** by Scrampunk — [https://freesound.org/people/Scrampunk/sounds/344696/](https://freesound.org/people/Scrampunk/sounds/344696/) — CC BY 4.0  
* `background_music.ogg`  
  **“Elf Harp”** by Awsapps — [https://freesound.org/people/Awsapps/sounds/628394/](https://freesound.org/people/Awsapps/sounds/628394/) — CC BY 4.0  
* `card_attack_sound_2.ogg`  
  **“Arrow_woosh__twang_01.wav”** by strangely_gnarled — [https://freesound.org/people/strangely_gnarled/sounds/72208/](https://freesound.org/people/strangely_gnarled/sounds/72208/) — CC BY 4.0  
* `card_attack_sound_1.ogg`  
  **“sword03.wav”** by Erdie — [https://freesound.org/people/Erdie/sounds/27857/](https://freesound.org/people/Erdie/sounds/27857/) — CC BY 4.0  

### 🔹 Creative Commons Attribution NonCommercial 4.0 (CC BY-NC 4.0)

* `endgame_music.ogg`  
  **“Suspense Ambiance Effect”** by Audio_Dread — [https://freesound.org/people/Audio_Dread/sounds/534572/](https://freesound.org/people/Audio_Dread/sounds/534572/) — CC BY-NC 4.0  
* `start_game_sound.ogg`  
  **“Mission of a Little Elf”** by Zankurō — [https://freesound.org/people/Zankur%C5%8D/sounds/435378/](https://freesound.org/people/Zankur%C5%8D/sounds/435378/) — CC BY-NC 4.0  

### 🔹 Creative Commons Attribution NonCommercial 3.0 (CC BY-NC 3.0)

* `boss_music.ogg`  
  **“Final boss music”** by fidsml — [https://freesound.org/people/fidsml/sounds/515683/](https://freesound.org/people/fidsml/sounds/515683/) — CC BY-NC 3.0  

### 🔹 Creative Commons Attribution 3.0 (CC BY 3.0)

* `heal_sound.ogg`  
  **“8bit_different.wav”** by Soundholder — [https://freesound.org/people/Soundholder/sounds/425337/](https://freesound.org/people/Soundholder/sounds/425337/) — CC BY 3.0  

### 🔹 Creative Commons 0 (CC0)

* `enemy_attack_sound.ogg`  
  **“Demonic Anger.wav”** by LilMati — [https://freesound.org/people/LilMati/sounds/527636/](https://freesound.org/people/LilMati/sounds/527636/) — CC0   

---

May your arrows fly true and your sword strike fast! 🌳🌟
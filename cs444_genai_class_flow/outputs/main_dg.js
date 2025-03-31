```javascript
import UI from './UI.js';
import GameLogic from './GameLogic.js';
import AudioManager from './AudioManager.js';

const assetPaths = {
    main_character_icon: 'outputs/main_character.png',
    enemy_icons: ['outputs/enemy_icon.png'],
    environment_background: 'outputs/environment_background.png',
    card_image: 'outputs/card_spell_vortex.png',
    menu_music: 'outputs/calm_mysterious_menu_music_901e47.mp3',
    background_music: 'outputs/dark_ambient_loop_music_cad249.mp3',
    victory_music: 'outputs/orchestral_triumphant_victory_620bcd.mp3',
    defeat_music: 'outputs/melancholic_defeat_piano_music_bc17e6.mp3',
    game_icon: 'outputs/game_icon.png',
    floor_texture: 'outputs/floor_texture.png'
};

function preloadAssets(paths) {
    const promises = [];

    for (const key in paths) {
        if (Array.isArray(paths[key])) {
            paths[key].forEach(path => {
                promises.push(loadAsset(path));
            });
        } else {
            promises.push(loadAsset(paths[key]));
        }
    }

    return Promise.all(promises);
}

function loadAsset(path) {
    return new Promise((resolve, reject) => {
        const extension = path.split('.').pop().toLowerCase();
        let asset;

        if (['png', 'jpg', 'jpeg', 'gif', 'bmp'].includes(extension)) {
            asset = new Image();
            asset.src = path;
            asset.onload = () => resolve(path);
            asset.onerror = () => reject(new Error(`Failed to load image: ${path}`));
        } else if (['mp3', 'wav', 'ogg'].includes(extension)) {
            asset = new Audio();
            asset.src = path;
            asset.onloadeddata = () => resolve(path);
            asset.onerror = () => reject(new Error(`Failed to load audio: ${path}`));
        } else {
            resolve(path);
        }
    });
}

window.addEventListener('load', async () => {
    try {
        await preloadAssets(assetPaths);

        const audioManager = new AudioManager(assetPaths);
        const gameLogic = new GameLogic();
        const ui = new UI();

        ui.initializeControls();
        gameLogic.initialize(ui, audioManager);

        console.log('Game initialized successfully.');
    } catch (error) {
        console.error('Error initializing game:', error);
    }
});
```
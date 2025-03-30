import { initializeUI } from './ui.js';
import { initializeLogic } from './logic.js';
import { initializeAudio } from './audio.js';
import { displayMainMenu } from './menu.js';
import { playMenuMusic } from './music.js';

document.addEventListener('DOMContentLoaded', () => {
    initializeUI();
    initializeLogic();
    initializeAudio();
    displayMainMenu();
    playMenuMusic();
});

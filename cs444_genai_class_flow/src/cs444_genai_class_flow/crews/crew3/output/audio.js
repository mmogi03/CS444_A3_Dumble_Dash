// JavaScript Audio Integration

// Load audio files
const cryptic_echoes = new Audio('C:\\Users\\hazem\\Documents\\GitHub\\CS444_A3_Dumble_Dash\\cs444_genai_class_flow\\src\\cs444_genai_class_flow\\crews\\crew2\\outputs\\cryptic_echoes_105b91.mp3');
const mystical_exploration = new Audio('C:\\Users\\hazem\\Documents\\GitHub\\CS444_A3_Dumble_Dash\\cs444_genai_class_flow\\src\\cs444_genai_class_flow\\crews\\crew2\\outputs\\mystical_exploration_3880f0.mp3');
const triumphant_victory = new Audio('C:\\Users\\hazem\\Documents\\GitHub\\CS444_A3_Dumble_Dash\\cs444_genai_class_flow\\src\\cs444_genai_class_flow\\crews\\crew2\\outputs\\triumphant_victory_45c59d.mp3');

// Set initial volume levels
cryptic_echoes.volume = 0.5;
mystical_exploration.volume = 0.5;
triumphant_victory.volume = 0.5;

// Enable looping for background music
cryptic_echoes.loop = true;
mystical_exploration.loop = true;

// Function to play audio based on game events
function playAudioForScene(scene) {
    switch(scene) {
        case 'mainMenu':
            cryptic_echoes.play();
            break;
        case 'exploration':
            mystical_exploration.play();
            break;
        case 'victory':
            triumphant_victory.play();
            break;
        default:
            console.log('No audio for this scene');
    }
}

// Example triggers for audio playback
function startGame() {
    document.getElementById('main-menu').classList.add('hidden');
    document.getElementById('game-hud').classList.remove('hidden');
    playAudioForScene('exploration'); // Play exploration music when the game starts
}

function endGameWithVictory() {
    playAudioForScene('victory'); // Play victory music when the game ends with a win
}

// Ensure only one track plays at a time
function stopAllAudio() {
    cryptic_echoes.pause();
    cryptic_echoes.currentTime = 0;
    mystical_exploration.pause();
    mystical_exploration.currentTime = 0;
    triumphant_victory.pause();
    triumphant_victory.currentTime = 0;
}

// Call stopAllAudio before playing a new track
function playAudioForScene(scene) {
    stopAllAudio();
    switch(scene) {
        case 'mainMenu':
            cryptic_echoes.play();
            break;
        case 'exploration':
            mystical_exploration.play();
            break;
        case 'victory':
            triumphant_victory.play();
            break;
        default:
            console.log('No audio for this scene');
    }
}
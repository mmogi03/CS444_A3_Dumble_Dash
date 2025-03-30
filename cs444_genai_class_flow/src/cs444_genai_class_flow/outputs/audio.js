```javascript
class AudioManager {
  constructor() {
    this.tracks = {
      menu: new Audio('audio/menu.mp3'),
      gameplay: new Audio('audio/gameplay.mp3'),
      victory: new Audio('audio/victory.mp3'),
      defeat: new Audio('audio/defeat.mp3')
    };
    this.currentTrack = null;
    this.initTracks();
  }

  initTracks() {
    for (let key in this.tracks) {
      this.tracks[key].loop = key === 'gameplay';
      this.tracks[key].volume = 0.5;
    }
  }

  playTrack(trackName) {
    if (this.currentTrack) {
      this.currentTrack.pause();
      this.currentTrack.currentTime = 0;
    }
    this.currentTrack = this.tracks[trackName];
    this.currentTrack.play();
  }

  stopAllMusic() {
    for (let key in this.tracks) {
      this.tracks[key].pause();
      this.tracks[key].currentTime = 0;
    }
    this.currentTrack = null;
  }

  setVolume(volume) {
    for (let key in this.tracks) {
      this.tracks[key].volume = volume;
    }
  }
}

// Usage
const audioManager = new AudioManager();

// Example triggers
function onMainMenu() {
  audioManager.playTrack('menu');
}

function onStartGame() {
  audioManager.playTrack('gameplay');
}

function onVictory() {
  audioManager.playTrack('victory');
}

function onDefeat() {
  audioManager.playTrack('defeat');
}

function onVolumeChange(newVolume) {
  audioManager.setVolume(newVolume);
}
```
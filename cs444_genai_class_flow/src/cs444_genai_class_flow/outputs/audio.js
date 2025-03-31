```javascript
class AudioManager {
    constructor() {
        this.audioTracks = {
            menu: new Audio('menu.mp3'),
            exploration: new Audio('background.mp3'),
            victory: new Audio('victory.mp3'),
            defeat: new Audio('defeat.mp3')
        };
        this.currentTrack = null;
        this.setVolume('menu', 0.5);
        this.setVolume('exploration', 0.7);
        this.setVolume('victory', 0.8);
        this.setVolume('defeat', 0.6);
        this.initEventListeners();
    }

    setVolume(track, volume) {
        if (this.audioTracks[track]) {
            this.audioTracks[track].volume = volume;
        }
    }

    playTrack(track) {
        if (this.currentTrack) {
            this.currentTrack.pause();
            this.currentTrack.currentTime = 0;
        }
        this.currentTrack = this.audioTracks[track];
        if (this.currentTrack) {
            this.currentTrack.loop = track === 'exploration';
            this.currentTrack.play();
        }
    }

    initEventListeners() {
        document.addEventListener('sceneChange', (event) => {
            const scene = event.detail.scene;
            this.playTrack(scene);
        });
    }
}

const audioManager = new AudioManager();
```
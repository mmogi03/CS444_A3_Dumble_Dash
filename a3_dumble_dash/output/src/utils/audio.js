export function setGlobalVolume(vol) {
    const audioElements = [
      document.getElementById("background-music"),
      document.getElementById("start-game-sound"),
      document.getElementById("end-game-music"),
      window.castleCutsceneBgm,
      window.castleCutsceneAudio
    ];
    audioElements.forEach((audio) => {
      if (audio) audio.volume = vol;
    });
}
  
export function fadeAudio(audio, targetVolume, duration, callback) {
    if (!audio) return;
    const initialVolume = audio.volume;
    const startTime = performance.now();
    function tick() {
      const elapsed = performance.now() - startTime;
      const fraction = Math.min(elapsed / duration, 1);
      audio.volume = initialVolume + (targetVolume - initialVolume) * fraction;
      if (fraction < 1) {
        requestAnimationFrame(tick);
      } else if (callback) {
        callback();
      }
    }
    tick();
}
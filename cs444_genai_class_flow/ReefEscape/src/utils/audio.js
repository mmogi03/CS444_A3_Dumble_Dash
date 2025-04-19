// src/utils/audio.js

export function setGlobalVolume(vol) {
  const level = parseFloat(vol);
  const audioElements = [
    document.getElementById("background-music"),
    document.getElementById("start-game-sound"),
    document.getElementById("end-game-music"),
    document.getElementById("audio-tail-whip"),
    document.getElementById("audio-tidal-splash"),
    document.getElementById("audio-coral-heal"),
    window.castleCutsceneBgm,
    window.castleCutsceneAudio
  ];

  audioElements.forEach((audio) => {
    if (!audio) return;
    // boost spell SFX by 20%, capped at 1.0
    const isSfx = [
      "audio-tail-whip",
      "audio-tidal-splash",
      "audio-coral-heal"
    ].includes(audio.id);
    const v = isSfx
      ? Math.min(level * 1.2, 1)
      : level;
    audio.volume = v;
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

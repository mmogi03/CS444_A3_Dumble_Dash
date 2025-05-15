import { showGameOver } from "../utils/battle.js";
import { updateScoreText } from "../utils/ui.js";

export default class BossScene extends Phaser.Scene {
  constructor() {
    super("BossScene");
  }

  create() {
    // hide battle-related UI elements and health/mana bars
    const battleUI = document.getElementById("battle-ui");
    // stop any overworld background music
    const bgMusic = document.getElementById("background-music");
    if (bgMusic) { bgMusic.pause(); bgMusic.currentTime = 0; }
    const enemyBar = document.getElementById("enemy-health-bar");
    const healthBar = document.getElementById("health-bar");
    const manaBar = document.getElementById("mana-bar");
    if (battleUI) battleUI.style.display = "none";
    if (enemyBar) enemyBar.style.display = "none";
    if (healthBar) healthBar.style.display = "none";
    if (manaBar) manaBar.style.display = "none";

    // background image
    const width = this.game.config.width;
    const height = this.game.config.height;
    // play background boss music
    this.bossBgm = this.sound.add("bossMusic", { loop: true, volume: 0.5 });
    this.bossBgm.play();

    this.add.image(width / 2, height / 2, "bossBackground").setDisplaySize(width, height);

    // mistakes counter 
    this.mistakes = 5;
    this.mistakesText = this.add.text(
      width - 20,
      20,
      `Mistakes: ${this.mistakes}`,
      { fontSize: '32px', color: '#FF0000' }
    ).setOrigin(1, 0);

    // generate random key sequence (length between 5 and 10)
    const minLength = 5;
    const maxLength = 10;
    const length = Phaser.Math.Between(minLength, maxLength);
    // explicit options list: letters (upper+lower), space, punctuation, numbers, symbols
    const options = [
      // uppercase letters
      'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
      // lowercase letters
      'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
      // whitespace and punctuation
      ' ','.',',','"',':',';','\'','}','{',']','[',
      // numbers
      '0','1','2','3','4','5','6','7','8','9',
      // symbols
      '!','@','#','$','%','^','&','*','(',')','-','_','+','=','|','\\','/','?','>','<'  
    ];
    this.sequence = [];
    for (let i = 0; i < length; i++) {
      this.sequence.push(options[Math.floor(Math.random() * options.length)]);
    }
    this.currentIndex = 0;

    // display sequence prompt centered with styling
    const promptText = "" + this.sequence.join(" → ");
    this.sequenceText = this.add.text(
      width / 2,
      height / 2,
      promptText,
      {
        fontSize: '64px',
        color: '#5E894D',
        padding: { x: 20, y: 10 }
      }
    ).setOrigin(0.5, 0.5);

    // set timer for sequence
    const baseTime = 30000;
    const reduction = ((window.currentLevel || 1) - 1) * 200;
    const maxTime = Math.max(2000, baseTime - reduction);
    // start timer event for boss fail
    this.timerEvent = this.time.delayedCall(maxTime, () => {
      this.failBoss();
    }, [], this);
    // setup timer UI in top left
    this.remainingTime = Math.ceil(maxTime / 1000);
    this.timeText = this.add.text(
      20,
      20,
      `Time: ${this.remainingTime}s`,
      { fontSize: '32px', color: '#FFC251' }
    ).setOrigin(0, 0);

    // create timer event to update UI every second
    this.time.addEvent({
      delay: 1000,
      callback: this.updateTimer,
      callbackScope: this,
      loop: true
    });

    // prepare options set for proper input filtering
    const optionsSet = new Set(options);

    // input listener (only track keys in options)
    this.input.keyboard.on('keydown', (event) => {
      const key = event.key;
      // ignore keys not part of the sequence options
      if (!optionsSet.has(key)) return;
      const expected = this.sequence[this.currentIndex];
      if (key === expected) {
        this.currentIndex++;
        if (this.currentIndex >= this.sequence.length) {
          this.winBoss();
        } else {
          const remaining = this.sequence.slice(this.currentIndex).join(" → ");
          this.sequenceText.setText(remaining);
        }
      } else {
        this.mistakes--;
        this.mistakesText.setText(`Mistakes: ${this.mistakes}`);
        if (this.mistakes <= 0) {
          this.failBoss();
        }
      }
    });
  }

  updateTimer() {
    if (this.remainingTime > 0) {
      this.remainingTime--;
      this.timeText.setText(`Time: ${this.remainingTime}s`);
    }
  }

  failBoss() {
    // stop boss music
    if (this.bossBgm) this.bossBgm.stop();
    showGameOver();
  }

  winBoss() {
    // cancel timer and input
    // stop boss music
    if (this.bossBgm) this.bossBgm.stop();
    if (this.timerEvent) this.timerEvent.remove(false);
    this.input.keyboard.removeAllListeners('keydown');
    // notify player
    this.sequenceText.setText("Boss Defeated!");
    // play victory sound
    this.sound.play("victorySnd", { volume: 1 });
    // add 300 points for defeating the boss
    const healthBar = document.getElementById("health-bar");
    const manaBar = document.getElementById("mana-bar");

    if (healthBar) healthBar.style.display = "block";
    if (manaBar) manaBar.style.display = "block";
    window.score += 300;
    updateScoreText();
    // prepare next dungeon level
    window.currentLevel = (window.currentLevel || 1) + 1;
    window.justFinishedBoss = false;
    // proceed to next dungeon level
    this.time.delayedCall(1000, () => {
      this.scene.start("OverworldScene");
    });
  }
} 
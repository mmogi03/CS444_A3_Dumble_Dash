```javascript
import { initializeUI } from './ui';
import { initializeLogic } from './logic';
import { initializeAudio } from './audio';
import { initializeScenes } from './scenes';

document.addEventListener('DOMContentLoaded', () => {
  initializeUI();
  initializeLogic();
  initializeAudio();
  initializeScenes();
});
```
export function generateMaze(width, height) {
    const maze = [];
    for (let y = 0; y < height; y++) {
      maze[y] = [];
      for (let x = 0; x < width; x++) {
        maze[y][x] = 1;
      }
    }
    function shuffle(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
      return array;
    }
    function carve(x, y) {
      maze[y][x] = 0;
      const directions = shuffle([[0, -2], [2, 0], [0, 2], [-2, 0]]);
      for (let [dx, dy] of directions) {
        const nx = x + dx;
        const ny = y + dy;
        if (nx > 0 && nx < width && ny > 0 && ny < height && maze[ny][nx] === 1) {
          maze[y + dy / 2][x + dx / 2] = 0;
          carve(nx, ny);
        }
      }
    }
    carve(1, 1);
    for (let y = 1; y < height - 1; y++) {
      for (let x = 1; x < width - 1; x++) {
        if (maze[y][x] === 1 && Math.random() < 0.1) {
          maze[y][x] = 0;
        }
      }
    }
    return maze;
}
  
export function getOpenCells(maze) {
    const openCells = [];
    for (let y = 0; y < maze.length; y++) {
      for (let x = 0; x < maze[y].length; x++) {
        if (maze[y][x] === 0) {
          openCells.push({ x, y });
        }
      }
    }
    return openCells;
}
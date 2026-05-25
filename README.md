# CaveDuster 💣

A minesweeper-inspired game built in Python with Pygame, made as a fun project to explore and implement classic algorithms hands-on.

## Algorithms & Design

The interesting parts under the hood:

- **Recursive flood-fill** — when you reveal a cell with no adjacent mines, it recursively uncovers all neighboring empty cells, chaining outward until it hits numbered boundary cells. Same idea as a paint bucket tool.
- **BFS-style neighbor exploration** — cell weights (the numbers) are computed by walking all 8 neighbors of every non-mine cell and counting adjacent mines.
- **Deferred mine placement** — mines aren't placed at game start. They're placed on your *first click*, guaranteeing you can never lose immediately. The clicked cell is always excluded from mine placement.
- **Shuffle queue** — the music player uses a proper shuffle queue rather than picking randomly each time, so every track plays once before anything repeats.

## Features

- 🎮 Mouse and controller support (tested on PXN Switch controller)
- 🚩 Left click to reveal, right click to flag
- 🎵 Sidebar music player with play/pause, prev/next, shuffle, and volume control
- ⏱ HUD with live mine counter and timer
- 🔄 Press `R` to restart at any time

## Setup

**Requirements**
```
pip install pygame
```

**Music**

Create a `game_music/` folder in the project root and drop any `.mp3` files into it. The game will load them all automatically as a playlist.

```
CaveDuster/
├── game_music/        ← put your songs here
├── main.py
├── mineGrid.py
├── cell.py
└── README.md
```

**Run**
```
python main.py
```

## Controls

| Input | Action |
|---|---|
| Left click | Reveal cell |
| Right click | Flag / unflag cell |
| R | Restart |
| Escape | Quit |
| D-pad | Move cursor |
| A button | Reveal cell |
| B button | Flag cell |
| Start button | Restart |
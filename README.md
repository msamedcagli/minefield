# Python Minesweeper

A classic Minesweeper game implemented in Python using Pygame.

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

1. Run the game:
```bash
python minesweeper.py
```

2. Game Controls:
- Left Click: Reveal a cell
- Right Click: Place/Remove a flag
- R Key: Reset the game

3. Game Rules:
- The game board is a 10x10 grid with 10 mines
- Numbers indicate how many mines are adjacent to each cell
- Use the numbers to deduce the locations of mines
- Flag cells where you think mines are located
- Reveal all non-mine cells to win
- Avoid clicking on mines!

## Features

- Classic Minesweeper gameplay
- Visual feedback for revealed cells and flags
- Game over and win conditions
- Easy reset functionality
- Clean and intuitive interface 
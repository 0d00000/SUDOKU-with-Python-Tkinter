# SUDOKU
[Video Demo](https://youtu.be/zBELUDkOb_g)
## Description:


This project is a **Sudoku game** built using Python's Tkinter library for the graphical user interface (GUI). The game offers multiple difficulty levels and an interactive Sudoku grid where players can solve puzzles with hints and progress tracking.

### Project Structure
```bash
SUDOKU
│
├── project.py              # Main script containing the game logic
├── test_project.py         # Test cases for the game
├── requirements.txt        # Required libraries for the project
└── README.md               # Project documentation

```

### Features

- **Difficulty Levels**: Choose from Easy, Medium, Hard, or Expert levels.
- **Sudoku Puzzle Generation**: Uses a backtracking algorithm to generate valid Sudoku puzzles.
- **Interactive Grid**: Click on cells to input numbers and track your progress.
- **Hints and Mistakes**: Players can use hints based on their level, but are limited to 3 mistakes.
- **Game Over and Win Conditions**: Game ends when all cells are correctly filled or after 3 mistakes.

#### Functions:

- `main()`: Initializes the Tkinter window for the Sudoku game.
- `validation(data: list, n: int, row: int, col: int) -> bool`: Validates whether a number can be placed at a specific cell of the Sudoku grid.
- `generate_Sudoku(data: list) -> bool`: Generates a valid Sudoku board using backtracking.
- `select_Level(frame: Frame)`: Displays the level selection menu for the Sudoku game.
- `start_Game(level: str)`: Starts the Sudoku game and sets up the initial game configuration based on the level.
- `GUI(data: list)`: Sets up the graphical user interface and displays the Sudoku game.
- `grid_set_up(data: list)`: Initializes the visual representation of the Sudoku grid.
- `on_entry(event, row: int, col: int)`: Handles user input in the entry fields of the Sudoku grid.
- `on_cell_click(event, row: int, col: int)`: Handles the visual state of the Sudoku grid if the user clicks a cell.
- `on_click_outside(event)`: Handles clicks outside of the Sudoku grid.
- `button_Check()`: Checks the player's current entries against the correct solution.
- `button_Restart()`: Restarts the Sudoku game by resetting the player's grid.
- `button_Hint()`: Provides a hint to the player by revealing a number in an empty cell.

### Requirements

- **Python**: Version 3.12.6
- **Tkinter**: Comes with Python /Tk version 8.2 used/
- **Random**: Comes with Python
- **Pytest**: Install using pip. To install required libraries:
```
$pip install -r requirements.txt
```
### How to Run the Game
Navigate to the project directory and run:
```bash
python project.py
```
### Testing
Run tests using pytest:
```bash
pytest test_project.py
```

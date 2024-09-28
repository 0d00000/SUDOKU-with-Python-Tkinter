from tkinter import *
import random

def main():
    """
    Initializes the Tkinter window for the Sudoku game.

    This function creates the main Tkinter window (`root`), sets its title and dimensions, 
    and calls the `select_Level` function to display the level selection menu. It then 
    enters the Tkinter main event loop.

    Global Variables:
        - root: The main Tkinter window object.
    """
    global root
    root = Tk()
    root.title("SUDOKU")
    root.geometry("550x400")                                                                                                                                                                                                                                                                                
    select_Level(Frame(root))
    root.mainloop()

def validation(data: list, n: int, row: int, col: int) -> bool:
    """
    Validates whether a number can be placed at a specific cell of the Sudoku grid.

    This function checks if the number `n` can be placed at the given location (row, col)                                                                                                                                                       
    in the `data` grid. It verifies that `n` does not already exist in the current row, 
    column, or the 3x3 subgrid.

    Args:
        data (list): A 9x9 list representing the Sudoku board.
        n (int): The number to placed in the grid.
        row (int): The row index where the number is to be placed.
        col (int): The column index where the number is to be placed.

    Returns:
        bool: True if the number can be placed, False otherwise.
    """
    if n in data[row]:
        return False
    if n in [data[r][col] for r in range(9)]:
        return False
    row_sub = (row//3)*3
    col_sub = (col//3)*3
    for r in range(row_sub, row_sub + 3):
        for c in range(col_sub, col_sub + 3):
            if data[r][c] == n:
                return False
    return True

def generate_Sudoku(data: list) -> bool:
    """
    Generate a valid Sudoku board using backtracking.

    This function attempts to fill the empty cells in the `data` grid with numbers 
    from 1 to 9 using backtracking. It calls the `validation` function to ensure 
    that any number placed does not violate Sudoku rules. If a placement leads to a 
    valid solution, it returns True; otherwise, it backtracks.

    Args:
        data (list): A 9x9 list representing the Sudoku grid (with None for empty cells).

    Returns:
        bool: True if the grid is successfully filled, False if no valid placement is possible.
    """
    for row in range(9):
        for col in range(9):
            if data[row][col] is None: # Empty Cell
                nums = list(range(1,10))
                random.shuffle(nums)
                for n in nums:
                    if validation(data, n, row, col):
                        data[row][col] = n
                        if generate_Sudoku(data):
                            return True
                        data[row][col] = None
                return False
    return True

def select_Level(frame: Frame):
    """
    Displays the level selection menu for the Sudoku game.

    This function creates a menubutton with various difficulty levels (Easy, Medium, Hard, 
    Expert) and associates each option with a command to start the game at that level by 
    calling the `start_Game` function. 

    Args:
        frame (Frame): The parent frame where the level selection menu will be displayed.

    Global Variables:
        - Label_level: A label widget indicating the current level selection.
    """
    global Label_level
    frame.pack(pady = 10)
    level = Menubutton(frame, text='level')
    level.menu = Menu(level)
    level["menu"] = level.menu
    level.menu.add_radiobutton(label="Easy", command=lambda: start_Game("Easy"))
    level.menu.add_radiobutton(label="Medium", command=lambda: start_Game("Medium"))
    level.menu.add_radiobutton(label="Hard", command=lambda: start_Game("Hard"))
    level.menu.add_radiobutton(label="Expert", command=lambda: start_Game("Expert"))
    level.pack()
    Label_level = Label(frame,text="Choose level", padx=10, pady=5)
    Label_level.pack()

def start_Game(level: str):
    """
    Starts the Sudoku game and sets up the initial game configuration based on the level.

    This function sets up the number of hints and empty cells according to the player's chosen 
    level. The `generate_sudoku` function is called to generate the puzzle grid and the solution,
    setting up important global variables for data organization throughout the game. Then, 
    the `GUI` function is called to display the game and the difficulty level.

    Args:
        level (str): The selected difficulty level ("Easy", "Medium", "Hard", or "Expert").

    Global Variables:
        - location: A list of coordinates representing the empty cells in the grid.
        - hint: The number of hints available based on the difficulty level.
        - Data_All: The fully solved Sudoku grid.
        - Data_Game: The initial Sudoku puzzle grid with some cells empty.
        - Data_Player: The grid containing the player's current progress.
    """
    global Label_level, level_text
    global location, hint, hint_or, Data_All, Data_Game, Data_Player
    location = []
    levels = {"Easy": {"location": 21, "hint": 2}, "Medium": {"location": 31, "hint": 3}, 
              "Hard": {"location": 41, "hint": 4}, "Expert": {"location": 51, "hint": 5}}
    num = random.randrange(levels[level]["location"],levels[level]["location"]+5,2)
    hint, hint_or, level_text = levels[level]["hint"], levels[level]["hint"], level
    Data_All = [[None]*9 for _ in range(9)]
    generate_Sudoku(Data_All)
    Data_Game = [row[:] for row in Data_All]
    while len(location) < num:
        r = random.randrange(9)
        c = random.randrange(9)
        if (r,c) not in location:
            location.append((r,c))
            Data_Game[r][c] = None
    location = sorted(location)
    Data_Player = [row[:] for row in Data_Game]
    GUI(Data_Game)
    Label_level.config(text=level)

def GUI(data: list):
    """
    Sets up the graphical user interface and display the Sudoku game.

    This function clears any existing widgets from the main window and creates a new interface
    that includes the Sudoku grid and control buttons. The `grid_set_up` function is called to
    display the current state of the Sudoku puzzle and binds mouse events for user interaction. 
    It also creates buttons for checking the solution, restarting the game, and using hints.

    Args:
        data (list): The Sudoku grid to be displayed.

    Global Variables:
        - Frame_grid: The frame containing the Sudoku grid.
        - Frame_main: The main frame of the game window.
        - hint: The number of hints remaining.
        - mistake: The current count of mistakes made by the player.
        - selected_cell: The currently selected cell in the Sudoku grid.
        - Button_hint: The button widget for using a hint.
        - Button_check: The button widget for checking the player's progress.
        - Button_nums: A list of button widgets for inputing numbers.
        - Label_mistake: A label displaying the number of mistakes.
        - Label_progress: A label displaying the player's progress in the game.
    """
    global Frame_grid, Frame_main
    global hint, mistake, selected_cell, color_progress
    global Button_hint, Button_check, Button_nums, Label_mistake, Label_progress

    for widget in root.winfo_children():
        widget.destroy()
    color = "grey"
    Frame_main = Frame(root, bg=color)
    Frame_main.pack(padx=10, pady=10, fill=BOTH, expand=True)
    # title
    Label_Title = Label(Frame_main, text="LET'S PLAY SUDOKU", font=("Chalkboard", 25), justify="center", bg=color, fg="white")
    Label_Title.pack(side=TOP, pady=10)
    # Sudoku
    Frame_grid = Frame(Frame_main, borderwidth=10, relief="ridge", bg="white")
    Frame_grid.pack(side=LEFT, padx=20)
    grid_set_up(data)
    root.bind("<Button-1>", on_click_outside)
    mistake = 0
    selected_cell = None
    Button_num = []

    Frame_buttons = Frame(Frame_main, borderwidth=10, relief="ridge")
    Frame_buttons.pack(side=RIGHT, padx=(0,20), pady=(0,5))
    Frame_buttons_buttons = Frame(Frame_buttons)
    Frame_buttons_buttons.pack(side=TOP, pady=10)
    select_Level(Frame_buttons_buttons)
    Button_check = Button(Frame_buttons_buttons, text="check", command= button_Check)
    Button_check.pack()
    Label_mistake = Label(Frame_buttons_buttons, text="mistake:0/3", font=("Times New Roman",12))
    Label_mistake.pack()
    Label_progress = Label(Frame_buttons_buttons, text="progress:0%", font=("Times New Roman",12))
    color_progress = Label_progress.cget("foreground")
    Label_progress.pack()
    Button_restart = Button(Frame_buttons_buttons, text="restart", command = button_Restart)
    Button_restart.pack(side=LEFT, padx=5)
    Button_hint = Button(Frame_buttons_buttons, text=f"hint:{hint}", command= button_Hint)
    Button_hint.pack(padx=(0,5))
    Frame_buttons_num = Frame(Frame_buttons)
    Frame_buttons_num.pack(side=BOTTOM, pady=(0,10))
    Button_nums = []
    for index, num in enumerate([i for i in range(1,10)]):
        Button_num = Button(Frame_buttons_num, text=str(num), command= lambda n = num: button_Number(n))
        Button_num.grid(row = index//3, column=index%3)
        Button_nums.append(Button_num)

def grid_set_up(data: list):
    """
    Initializes the visual representation of the Sudoku grid.

    This function creates the grid of cells in the GUI, determining whether each cell is a label
    (for pre-filled numbers) or an entry field (for user input). The provided `data` is used to
    set the initial values of the cells and binds events for user interaction. It also saves the 
    original background, foreground colors and state (noraml/disabled) for resetting purposes.

    Args:
        data (list): The Sudoku grid to be displayed.

    Global Variables:
        - entries: A 2D list of widgets representing the cells in the grid.
        - or_bg: A 2D list storing the original background color of each cell.
        - or_fg: A 2D list storing the original foreground color of each cell.
        - or_st: A 2D list storing the original state (normal/disabled) of each cell.
    """
    global Frame_grid, entries, or_bg, or_fg, or_st
    or_bg = [[None]*9 for _ in range(9)]
    or_fg = [[None]*9 for _ in range(9)]
    or_st = [[None]*9 for _ in range(9)]
    entries = [[None]*9 for _ in range(9)]
    font = ('Chewy', 15)
    for row in range(9):
        for col in range(9):
            color_bg = "lightgrey" if (row//3 + col//3)%2 == 0 else "white"
            if (row,col) not in location:
                cell = Label(Frame_grid, width=2, text=str(data[row][col]), font=font, justify='center', relief="flat", bg = color_bg, fg="black")
            else:
                cell = Entry(Frame_grid, width=2, font=font, justify='center', relief="flat", highlightthickness=0, bg=color_bg, fg="blue")
                cell.bind("<KeyRelease>", lambda e, r = row, c = col: on_entry(e,r,c))
            entries[row][col] = cell
            cell.grid(row = row, column=col, padx=1, pady=1)
            cell.bind("<Button-1>", lambda e, r=row, c=col: on_cell_click(e, r, c))

            or_bg[row][col] = cell.cget("background")
            or_fg[row][col] = cell.cget("foreground")
            or_st[row][col] = cell.cget("state")

def on_entry(event, row: int, col: int):  
    """
    Handles user input in the entry fields of the Sudoku grid.

    This function is triggered when a user types into an entry cell. If the input is valid 
    (an integer between 1 and 9), it updates the `Data_Player` list and calls `button_Disable` 
    to disable the corresponding number button if the maximum number of that value is reached. 
    If the input is invalid, it resets the cell's value.

    Args:
        event: The Tkinter event representing the player's key press.
        row (int): The row index of the selected cell.
        col (int): The column index of the selected cell.
    """
    try:
        value = int(event.widget.get())
    except ValueError:
        old_value = Data_Player[row][col]
        if old_value:
            Data_Player[row][col] = None
            button_Disable(old_value)
        event.widget.delete(0, END)
        return
    if 1 <= value <= 9:
        old_value = Data_Player[row][col]
        Data_Player[row][col] = value
        button_Disable(value)
        if old_value:
            button_Disable(old_value)
    else:
        event.widget.delete(0, END)
        Data_Player[row][col] = None
    

def on_cell_click(event, row: int, col: int):
    """
    Handles the visual state of the Sudoku grid if user clicks a cell.

    This function highlights the clicked cell and its corresponding row, column, and 
    3x3 sub-grid by changing their color. It also updates the `selected_cell` variable
    to track the current cell being edited.

    Args:
        event: The Tkinter event representing the mouse click.
        row (int): The row index of the clicked cell.
        col (int): The column index of the clicked cell.

    Global Variables:
        - selected_cell: The currently selected cell
    """
    global selected_cell
    selected_cell = (row,col)
    selected_num = Data_Player[row][col]
    cell_reset()
    for r in range(9):
        for c in range(9):
            if Data_Player[r][c] == selected_num and Data_Player[r][c] is not None:
                entries[r][c].config(state='normal', bg='lightblue', fg='magenta')
    for i in range(9):
        entries[i][col].config(state='normal', bg='lightblue', fg='black')
        entries[row][i].config(state='normal', bg='lightblue', fg='black')
    sub_row = 3 * (row // 3)
    sub_col = 3 * (col // 3)
    for r in range(sub_row, sub_row + 3):
        for c in range(sub_col, sub_col + 3):
            entries[r][c].config(state='normal', bg='lightblue', fg='black')
    entries[row][col].config(fg='magenta')
    entries[row][col].focus_set()

def on_click_outside(event):
    """
    Handles clicks outside of the Sudoku grid.

    This function resets the state of the cells if a click is detected outside the grid, and
    calls `cell_reset` function allowing for a cleaner user interface.

    Args:
        event: The Tkinter event representing the mouse click.
    """
    if not(Frame_grid.winfo_rootx() <= event.x_root <= Frame_grid.winfo_rootx() + Frame_grid.winfo_width() and
           Frame_grid.winfo_rooty() <= event.y_root <= Frame_grid.winfo_rooty() + Frame_grid.winfo_height()):
        cell_reset()

def button_Check():
    """
    Checks the player's current entries against the correct solution.

    This function compares the player's entries in `Data_Player` with the `Data_All`. Then updates
    the mistake count for incorrect entries and displays the player's progress as a percentage. 
    If the solution is correct, it ends the game with a win message. If the player makes three 
    mistakes, it ends the game with a "Game Over" message.

    Global Variables:
        - mistake: The current count of mistakes made by the player.
        - Frame_grid: The frame containing the Sudoku grid.
        - Frame_main: The main frame of the game window.
        - Data_Player: The grid containing the player's current entries.
        - Data_All: The correct solution grid.
        - Label_mistake: A label displaying the number of mistakes.
        - Label_progress: A label displaying the player's progress in percentage.
        - Button_hint: The button for using hints (disabled on game end).
        - Button_check: The button for checking the player's solution (disabled on game over).
    """

    global mistake, color_progress, Frame_grid, Frame_main
    progress = 0
    w = Frame_grid.winfo_width()
    h = Frame_grid.winfo_height()
    for (row, col) in location:
        if Data_Player[row][col] is not None:
            if Data_Player[row][col] != Data_All[row][col]:
                mistake += 1
                entries[row][col].config(bg="lightpink", fg="red")
        if Data_Player[row][col] == Data_All[row][col]:
            progress += 1
    progress = round(100*progress/len(location))
    color_p = color_progress if progress <= 50 else ("orange" if progress <= 90 else "green")
    Label_mistake.config(text = f"mistake:{mistake}/3")
    Label_progress.config(text = f"progress:{progress}%", fg=color_p)
    if all(Data_Player[row][col] == Data_All[row][col] for (row,col) in location):
        Frame_grid.destroy()
        Button_hint.config(state="disabled")
        Frame_grid = Frame(Frame_main, bg="white", width=w, height=h)
        Frame_grid.pack(side=LEFT, padx=20)
        Frame_grid.pack_propagate(False)
        game_over = Label(Frame_grid, text="YOU WIN 🎉🎉🎉", font=("Impact",36,"bold"),bg="green")
        game_over.pack(expand=True)
    elif mistake >= 3:
        Frame_grid.destroy()
        Button_hint.config(state="disabled")
        Button_check.config(state="disabled")
        Label_mistake.config(text="mistake:3/3", fg="grey")
        Frame_grid = Frame(Frame_main, bg="white", width=w, height=h)
        Frame_grid.pack(side=LEFT, padx=20)
        Frame_grid.pack_propagate(False)
        game_over = Label(Frame_grid, text="GAME OVER", font=("Impact",36,"bold"),bg="red")
        game_over.pack(expand=True)
        
def button_Restart():
    """
    Restarts the Sudoku game by resetting the player's grid.

    This function resets the `Data_Player` grid to its original state and reinitializes the list of 
    empty cell locations. The `GUI` function is called to update the interface with the new game state.

    Global Variables:
        - Data_Player: The grid containing the player's current entries.
        - Data_Game: The initial Sudoku puzzle grid with some cells empty.
        - location: The list of coordinates representing the empty cells.
    """
    global hint, hint_or, level_text, Data_Player, Data_Game, location
    hint = hint_or
    Data_Player = [row[:] for row in Data_Game]
    location = [(r,c) for r in range(9) for c in range(9) if Data_Game[r][c] is None]
    GUI(Data_Game)
    Label_level.config(text=level_text)
    
def button_Hint():
    """
    Provides a hint to the player by revealing a number in an empty cell.

    This function either fills the currently selected empty cell or a random empty cell with 
    the correct value from `Data_All`. It decreases the hint count, and disables the hint
    button when no hints are remaining.

    Global Variables:
        - hint: The number of hints remaining.
        - selected_cell: The currently selected cell in the Sudoku grid.
        - location: The list of coordinates representing the empty cells.
        - Data_All: The correct solution grid.
        - Data_Player: The grid containing the player's current entries.
        - Button_hint: The button for using a hint (disabled when no hints remain).
    """

    global hint
    if selected_cell and selected_cell in location:
        r,c = selected_cell
    else:
        r,c = random.choice(location)
    location.remove((r,c))
    value = Data_All[r][c]
    Data_Player[r][c] = value
    
    entries[r][c].destroy()  # Remove the existing Entry widget
    color = "lightgrey" if (r//3 + c//3)%2 == 0 else "white"
    cell = Label(Frame_grid, width=2, text=str(value), font=('Chewy', 15), justify='center', relief="flat", bg=color, fg="blue")
    cell.grid(row=r, column=c, padx=1, pady=1)
    cell.bind("<Button-1>", lambda e, r=r, c=c: on_cell_click(e, r, c))
    entries[r][c] = cell 

    hint -= 1
    Button_hint.config(text = f"hint:{hint}")
    if hint == 0:
        Button_hint.config(state="disabled")
    
def button_Number(num: int):
    """
    Handles the input of a number button and fills the selected cell in the grid.

    This function modifies the value of the currently selected cell based on user input 
    from the number buttons. It also checks for mistakes and updates the display accordingly.

    Args:
        num (int): The number selected by the player.

    Global Variables:
        - mistake: The current count of mistakes made by the player.
        - selected_cell: The currently selected cell in the Sudoku grid.
        - Button_nums: A list of buttons representing the numbers 1-9.
    """
    global mistake
    if selected_cell:
        row, col = selected_cell
        if (row, col) in location:
            entries[row][col].delete(0,END)
            entries[row][col].insert(END, str(num))
        Data_Player[row][col] = num
        if num != Data_All[row][col]:
            mistake += 1
            entries[row][col].config(bg="lightpink", fg="red")
        Label_mistake.config(text = f"mistake:{mistake}/3")
        button_Disable(num)

def button_Disable(num: int):
    """
    Disables the number button when all instances of the number have been placed.

    This function checks how many times the number `num` has been placed in the player's grid 
    (`Data_Player`). If the count reaches 9, the corresponding number button is disabled.

    Args:
        num (int): The number to check and disable if fully placed.

    Global Variables:
        - Button_nums: A list of buttons representing the numbers 1-9.
        - Data_Player: The grid containing the player's current entries.
    """
    global Button_nums
    count = sum(row.count(num) for row in Data_Player)
    if count >= 9:
        Button_nums[num-1].config(state="disabled")
    else:
        Button_nums[num-1].config(state="normal")

def cell_reset():
    """
    Resets the visual state of the Sudoku grid.

    This function resets the background color, text color, and state (enabled/disabled) of 
    all cells in the Sudoku grid to their original values (`or_bg`, `or_fg`, `or_st`).

    Global Variables:
        - entries: A 2D list of widgets representing the cells in the grid.
        - or_bg: A 2D list storing the original background color of each cell.
        - or_fg: A 2D list storing the original foreground color of each cell.
        - or_st: A 2D list storing the original state (normal/disabled) of each cell.
    """

    for row in range(9):
        for col in range(9):
            if entries[row][col].winfo_exists():
                entries[row][col].config(bg = or_bg[row][col], fg = or_fg[row][col], state = or_st[row][col])

    
if __name__ == "__main__":
    main()
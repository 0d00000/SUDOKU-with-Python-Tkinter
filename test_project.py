from tkinter import *
from unittest.mock import patch
from project import validation, generate_Sudoku
from project import select_Level, start_Game

root = Tk()
frame = Frame(root)
frame.pack()
data = [
    [5, 3, None, None, 7, None, None, None, None],
    [6, None, None, 1, 9, 5, None, None, None],
    [None, 9, 8, None, None, None, None, 6, None],
    [8, None, None, None, 6, None, None, None, 3],
    [4, None, None, 8, None, 3, None, None, 1],
    [7, None, None, None, 2, None, None, None, 6],
    [None, 6, None, None, None, None, 2, 8, None],
    [None, None, None, 4, 1, 9, None, None, 5],
    [None, None, None, None, 8, None, None, 7, 9],
]

def test_validation():
    assert validation(data,5,0,2) == False
    assert validation(data,1,0,2) == True

def test_generate_Sudoku():
    data = [[None]*9 for _ in range(9)]
    data_bool = generate_Sudoku(data)
    assert data_bool == True

    for row in data:
        for cell in row:
            assert 1 <= cell <= 9
        assert sorted(row) == list(range(1,10))

    for col in range(9):
        column = [data[row][col] for row in range(9)]
        assert sorted(column) == list(range(1,10))
    
    for sub_row in range(0,9,3):
        for sub_col in range(0,9,3):
            sub_grid = []
            for row in range(sub_row, sub_row + 3):
                for col in range(sub_col, sub_col + 3):
                    sub_grid.append(data[row][col])
            assert sorted(sub_grid) == list(range(1,10))

def test_select_Level():
    mock_start_game = patch('project.start_Game').start()
    
    select_Level(frame)
    level_button = None
    for widget in frame.winfo_children():
        if isinstance(widget, Menubutton):
            level_button = widget
            break
    assert level_button is not None

    menu = level_button.menu
    assert "Easy" in menu.entrycget(0, 'label')
    assert "Medium" in menu.entrycget(1, 'label')
    assert "Hard" in menu.entrycget(2, 'label')
    assert "Expert" in menu.entrycget(3, 'label')

    menu.invoke(3)
    mock_start_game.assert_called_once_with("Expert")
    patch.stopall()

def test_start_Game():
    mock_gui = patch('project.GUI').start()
    start_Game("Easy")
    mock_gui.assert_called_once()
    called_args = list(mock_gui.call_args[0])
    assert len(called_args[0]) == 9
    assert all(len(row) == 9 for row in called_args[0])
    levels = {"Easy": 21, "Medium": 31, "Hard": 41, "Expert": 51}
    count = sum(1 for row in called_args[0] for cell in row if cell is None)
    assert count in range(levels["Easy"], levels["Easy"] + 5,2)
    patch.stopall()

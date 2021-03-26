import copy

board = [[0, 0, 4, 6, 7, 2, 0, 0, 0],
         [5, 0, 0, 8, 0, 0, 0, 9, 6],
         [0, 6, 3, 0, 4, 0, 0, 0, 8],
         [3, 8, 2, 1, 0, 0, 9, 6, 0],
         [4, 7, 5, 0, 0, 0, 1, 0, 0],
         [9, 1, 0, 2, 0, 4, 5, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 2, 9],
         [0, 0, 1, 0, 0, 0, 7, 4, 3],
         [2, 0, 0, 0, 6, 3, 8, 0, 1]]

temp = copy.deepcopy(board) # copy of board is used to check the solver output with the player's board

def make_move(row, column, number):
    """user chooses which row and column that he wants to add the number in."""
    board[row - 1][column - 1] = number
    return board

def printBoard(board):
    """prints board in human readable form"""
    dividers = "|--------------------------------|"
    print(dividers)
    for rows in range(0,9):
        for columns in range(0,9):
            if (rows == 3 or rows == 6) and columns == 0:
                print(dividers)
            if columns == 0 or columns == 3 or columns == 6:
                print("|", end=" ")
            print(" " + str(board[rows][columns]), end=" ")
            if columns == 8:
                print("|")
    print(dividers)
    return

def empty_space(board):
    """helper function for solver. looks for empty space on board"""
    for row in range(0, 9):
        for column in range(0, 9):
            if board[row][column] == 0:
                return row, column
    return None, None

def correct_move(board, row, column, number):
    """checks if the number inputted is a correct move to do. Works primarly with the solver function in terms of
    backtracking"""
    # checks if number appears in the same row
    for i in range(0,9):
        if board[row][i] == number:
            return False
    # checks if number appears in the same column
    for i in range(0,9):
        if board[i][column] == number:
            return False
    # checks if number appears in the same square
    square_row = (row//3) * 3
    square_column = (column//3) * 3
    for i in range(0,3):
        for j in range(0,3):
            if board[square_row + i][square_column + j] == number:
                return False
    return True

def solve_board(board):
    """contains two helper functions that help find the next empty space and check if number is the correct move. Updates
    the main board if the sudoku puzzle is solvable"""
    # finds the first available empty space
    row, column = empty_space(board)
    if row is None: # checks if board is filled up
        return True
    for number in range(1, 10): # the range of numbers available 1, 2, 3, .... 9
        if correct_move(board, row, column, number): # checks if it's a correct move then inputs number at position
            board[row][column] = number
            if solve_board(board): # recursively call our function
                return True
        # if number ends up being not valid, we need to backtrack and try another number
        board[row][column] = 0
    return False # return false if sudoku cannot be solved

def check_solved(player_board):
    """checks if player solved the sudoku right by comparing the solver with the inputted player board"""
    solve_board(temp)
    if board != temp:
        return "Not Solved, Try Again!"
    else:
        return "Solved!"

print("Showing the user being able to solve the puzzle and show if it's complete")
make_move(1, 1, 8)
make_move(1, 2, 9)
make_move(1, 7, 3)
make_move(1, 8, 1)
make_move(1, 9, 5)
make_move(2, 2, 2)
make_move(2, 3, 7)
make_move(2, 5, 3)
make_move(2, 6, 1)
make_move(2, 7, 4)
make_move(3, 1, 1)
make_move(3, 4, 5)
make_move(3, 6, 9)
make_move(3, 7, 2)
make_move(3, 8, 7)
make_move(4, 5, 5)
make_move(4, 6, 7)
make_move(4, 9, 4)
make_move(5, 4, 3)
make_move(5, 5, 9)
make_move(5, 6, 6)
make_move(5, 8, 8)
make_move(5, 9, 2)
make_move(6, 3, 6)
make_move(6, 5, 8)
make_move(6, 8, 3)
make_move(6, 9, 7)
make_move(7, 1, 7)
make_move(7, 2, 3)
make_move(7, 3, 8)
make_move(7, 4, 4)
make_move(7, 5, 1)
make_move(7, 6, 5)
make_move(7, 7, 6)
make_move(8, 1, 6)
make_move(8, 2, 5)
make_move(8, 4, 9)
make_move(8, 5, 2)
make_move(8, 6, 8)
make_move(9, 2, 4)
make_move(9, 3, 9)
make_move(9, 4, 7)
make_move(9, 8, 5)
printBoard(board)
print(check_solved(board))
make_move(9, 8, 2)
printBoard(board)
print(check_solved(board))


print("BONUS: Here's the solver finding the solution to a different sudoku puzzle immediately")
bonus = [[2, 0, 0, 3, 6, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 3, 0],
         [0, 0, 3, 2, 4, 0, 0, 9, 0],
         [0, 2, 7, 0, 0, 0, 0, 1, 0],
         [0, 3, 1, 6, 0, 0, 9, 0, 0],
         [6, 0, 9, 8, 1, 0, 2, 0, 7],
         [9, 6, 2, 4, 0, 0, 3, 0, 0],
         [1, 0, 5, 0, 3, 0, 4, 2, 0],
         [3, 7, 4, 0, 8, 2, 5, 6, 0]]
solve_board(bonus)
printBoard(bonus)
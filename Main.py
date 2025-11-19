import itertools
import sys
from itertools import combinations
board = [8, 1, 6, 3, 5, 7, 4, 9, 2]
X_move = []
O_move = []
magic_number = '15'
moves = 9
final_combo_list = []
final_combo_O_list = []
def check():
    if magic_number in final_combo:
        input("X won!")
        quit()
def check_O():
    if magic_number in final_combo_O:
        input("O won!")
        quit()
def print_board():
    print(f"{board[0]}  {board[1]}  {board[2]}")
    print(f"{board[3]}  {board[4]}  {board[5]}")
    print(f"{board[6]}  {board[7]}  {board[8]}")
print()
print_board()
while moves > 0:
    while True:
        X_input = input("enter a number on the square(X side)   ")
        if X_input .isdigit() == True:
            break
        else:
            print_board()
            print("enter a valid number!")
    X_input = int(X_input)
    if X_input == 1:
        board[1] = 'X'
        X_move.append(X_input)
    elif X_input == 2:
        board[8] = 'X'
        X_move.append(X_input)
    elif X_input == 3:
        board[3] = 'X'
        X_move.append(X_input)
    elif X_input == 4:
        board[6] = 'X'
        X_move.append(X_input)
    elif X_input == 5:
        board[4] = 'X'
        X_move.append(X_input)
    elif X_input == 6:
        board[2] = 'X'
        X_move.append(X_input)
    elif X_input == 7:
        board[5] = 'X'
        X_move.append(X_input)
    elif X_input == 8:
        board[0] = 'X'
        X_move.append(X_input)
    elif X_input == 9:
        board[7] = 'x'
        X_move.append(X_input)
    print_board()
    moves -= 1
    if moves == 0:
        break
    if len(X_move) >= 3:
        three_elements_combo = (combinations(X_move, 3))
        for win_combo in three_elements_combo:
            final_combo = win_combo[0] + win_combo[1] + win_combo[2]
            final_combo = str(final_combo)
            final_combo_list.append(final_combo)
            check()
    while True:
        O_input = input("enter a number on the square(O side)   ")
        if O_input.isdigit() == True:
            break
        else:
            print_board()
            print("enter a valid number!")
    O_input = int(O_input)
    if O_input == 1:
        board[1] = 'O'
        O_move.append(O_input)
    elif O_input == 2:
        board[8] = 'O'
        O_move.append(O_input)
    elif O_input == 3:
        board[3] = 'O'
        O_move.append(O_input)
    elif O_input == 4:
        board[6] = 'O'
        O_move.append(O_input)
    elif O_input == 5:
        board[4] = 'O'
        O_move.append(O_input)
    elif O_input == 6:
        board[2] = 'O'
        O_move.append(O_input)
    elif O_input == 7:
        board[5] = 'O'
        O_move.append(O_input)
    elif O_input == 8:
        board[0] = 'O'
        O_move.append(O_input)
    elif O_input == 9:
        board[7] = 'O'
        O_move.append(O_input)
    print_board()
    moves -= 1
    if moves == 0:
        break
    if len(O_move) >= 3:
        three_elements_combo_O = (combinations(O_move, 3))
        for win_combo_O in three_elements_combo_O:
            final_combo_O = win_combo_O[0] + win_combo_O[1] + win_combo_O[2]
            final_combo_O = str(final_combo_O)
            final_combo_list.append(final_combo_O)
            check_O()
input("draw!")

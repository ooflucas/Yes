import random
import sys
pos = [' '] * 25
steps = []
mine_pos = []
def print_board(row, column):
    print(f'| {pos[0]} | {pos[1]} | {pos[2]} | {pos[3]} | {pos[4]} |')
    print(f'---------------------')
    print(f'| {pos[5]} | {pos[6]} | {pos[7]} | {pos[8]} | {pos[9]} |')
    print(f'---------------------')
    print(f'| {pos[10]} | {pos[11]} | {pos[12]} | {pos[13]} | {pos[14]} |')
    print(f'---------------------')
    print(f'| {pos[15]} | {pos[16]} | {pos[17]} | {pos[18]} | {pos[19]} |')
    print(f'---------------------')
    print(f'| {pos[20]} | {pos[21]} | {pos[22]} | {pos[23]} | {pos[24]} |')
    print(f'---------------------')
def generate_mine():
    for mines in range(3,5):
        pos[mines] = '*'
        mine_pos.append(mines)
def find_adjacent_cells(positions):
    offsets = [-5, 5, -1, 1, -6, -4, 4, 6]
    adjacent_list = []
    positions = int(positions)
    upper = positions - 5
    lower = positions + 5
    left = positions - 1
    right = positions + 1
    upper_left = positions - 6
    upper_right = positions - 4
    lower_left = positions + 4
    lower_right = positions + 6
    adjacent_list = [upper, lower, left, right, upper_left, upper_right, lower_left, lower_right]
    return adjacent_list
def step():
    position = input('enter a position to step on:   ')
    position = int(position)
    mine_adjacent = 0
    print(find_adjacent_cells(position))
    adjacent_list = find_adjacent_cells(position)
    for adj_cell in adjacent_list:
        if adj_cell in mine_pos:
            mine_adjacent += 1
    pos[position] = mine_adjacent
    if position in mine_pos:
        print('you lost!')
        sys.exit
        return
    steps.append(position)
generate_mine()
while True:
    print_board()
    step()

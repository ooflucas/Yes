import random
import sys
left_counter = 1
right_counter = 10
column = 10
row = 5
pos = [' '] * column * row * 2
steps = []
mine_pos = []
def print_board(column, row):
    for i in range(column*row):
        i = i+1
        print('|', pos[i],'|', end = '')
        if i % column == 0:
            print('\n','-----'*column)
def generate_mine():
    for mines in range(3,5):
        pos[mines] = '*'
        mine_pos.append(mines)
def corners():
    corner = []
    global column
    global row
    corner.append(1)
    corner.append(column)
    corner.append(column*(row-1)+1)
    corner.append(column*row)
    print(corner)
    return corner
def sides():
    side_list = []
    left_side = []
    right_side = []
    bottom_side = []
    top_side = []
    global column
    global row
    corner = corners()
    for top in range(column):
        top += 1
        if top in corner:
            continue
        top_side.append(top)
    print(f"top = {top_side}")
    for bottom in range(column*(row-1), column*row):
        bottom += 1
        if bottom in corner:
            continue
        bottom_side.append(bottom)
    print(f"bottom = {bottom_side}")
    for left in range(column):
        left += 1
        left += column
        if left in corner:
            continue
        left_side.append(left)
    print(f"left = {left_side}")
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
    print('\n')
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
    print_board(column, row)
    sides()
    step()

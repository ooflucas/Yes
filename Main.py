import random
import sys
left_counter = 1
right_counter = 10
column = 5
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
    global column
    global row
    top_right_corner = 1
    top_left_corner = column
    bottom_right_corner = (column*(row-1)+1)
    bottom_left_corner = (column*row)
    return top_right_corner, top_left_corner, bottom_right_corner, bottom_left_corner
def sides():
    side_list = []
    left_side = []
    right_side = []
    bottom_side = []
    top_side = []
    topright, topleft, bottomright, bottomleft = corners()
    corner = [topright, topleft, bottomright, bottomleft]
    global column
    global row
    for top in range(column):
        top += 1
        if top in corner:
            continue
        top_side.append(top)
    for bottom in range(column*(row-1), column*row):
        bottom += 1
        if bottom in corner:
            continue
        bottom_side.append(bottom)
    for right in range(row):
        right += 1
        right = right*column
        if right in corner:
            continue
        right_side.append(right)
    lef = 1
    for left in range(row-1):
        lef += column
        if lef in corner:
            continue
        left_side.append(lef)
    return top_side, bottom_side, left_side, right_side
def find_adjacent_cells(positions):
    top, bottom, left, right = sides()
    top_right, top_left, bottom_right, bottom_left = corners()
    print(f'top = {top}')
    print(f'bottom = {bottom}')
    print(f'left = {left}')
    print(f'right = {right}')
    print(f'top right = {top_right}')
    print(f'top left = {top_left}')
    print(f'bottom right = {bottom_right}')
    print(f'bottom left = {bottom_left}')
    print('\n')
    adjacent_list = []
    positions = int(positions)
    if positions in top_right:
        right = positions + 1
        lower = positions + column
        lower_right = positions + column
    elif positions in top_left:
        left = positions - 1
        lower = positions + column
        lower_left = positions + column - 1
    upper = positions - column
    lower = positions + column
    left = positions - 1
    right = positions + 1
    upper_left = positions - column+1
    upper_right = positions - column-1
    lower_left = positions + column-1
    lower_right = positions + column+1
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
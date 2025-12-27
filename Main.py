import random
import sys
column = 5
row = 5
pos = [' '] * column * row * 2
steps = []
mine_pos = []
flags = []
moves = 0
def print_board(column, row):
    for i in range(column*row):
        i = i+1
        print('|', pos[i],'|', end = '')
        if i % column == 0:
            print('\n','-----'*column)
def generate_mine():
    global row
    global column
    mines = random.sample(range(1, row*column), round(row*column*0.3))
    for i in range(len(mines)):
        pos[mines[i]] = ' '
        mine_pos.append(mines[i])
def corners():
    global column
    global row
    top_left_corner = 1
    top_right_corner = column
    bottom_left_corner = (column*(row-1)+1)
    bottom_right_corner = (column*row)
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
    topside, bottomside, leftside, rightside = sides()
    top_right, top_left, bottom_right, bottom_left = corners()
    print(f'top = {topside}')
    print(f'bottom = {bottomside}')
    print(f'left = {leftside}')
    print(f'right = {rightside}')
    print(f'top right = {top_right}')
    print(f'top left = {top_left}')
    print(f'bottom right = {bottom_right}')
    print(f'bottom left = {bottom_left}')
    print('\n')
    adjacent_list = []
    positions = int(positions)
    if positions == top_right:
        left = positions - 1
        lower = positions + column
        lower_left = positions + column - 1
        adjacent_list = [lower, left, lower_left]
        return adjacent_list
    elif positions == top_left:
        right = positions + 1
        lower = positions + column
        lower_right = positions + column + 1
        adjacent_list = [right, lower, lower_right]
        return adjacent_list
    elif positions == bottom_left:
        upper = positions - column
        upper_right = positions - column + 1
        right = positions + 1
        adjacent_list = [upper, upper_right, right]
        return adjacent_list
    elif positions == bottom_right:
        left = positions - 1
        upper = positions + column
        upper_left = positions + column - 1
        adjacent_list = [left, upper, upper_left]
        return adjacent_list
    elif positions in topside:
        lower = positions + column
        left = positions - 1
        right = positions + 1
        lower_left = positions + column - 1
        lower_right = positions + column + 1
        adjacent_list = [lower, left, right, lower_left, lower_right]
        return adjacent_list
    elif positions in bottomside:
        upper = positions - column
        left = positions - 1
        right = positions + 1
        upper_left = positions - column - 1
        upper_right = positions - column + 1
        adjacent_list = [upper, left, right, upper_left, upper_right]
        return adjacent_list
    elif positions in leftside:
        upper = positions - column
        lower = positions + column
        right = positions + 1
        upper_right = positions - column + 1
        lower_right = positions + column + 1
        adjacent_list = [upper, lower, right, upper_right, lower_right]
        return adjacent_list
    elif positions in rightside:
        upper = positions - column
        lower = positions + column
        left = positions - 1
        upper_left = positions - column - 1
        lower_left = positions + column - 1
        adjacent_list = [upper, lower, left, upper_left, lower_left]
        return adjacent_list
    else:
        upper = positions - column
        lower = positions + column
        left = positions - 1
        right = positions + 1
        upper_left = positions - column - 1
        upper_right = positions - column + 1
        lower_left = positions + column - 1
        lower_right = positions + column + 1
        adjacent_list = [upper, lower, left, right, upper_left, upper_right, lower_left, lower_right]
        return adjacent_list
def step():
    global column
    global row
    global flags
    global moves
    print_board(column, row)
    while True:
        print('\n')
        position = input('enter a position:   ')
        if not int(position) in flags:
            break
        else:
            print("this position is flagged!")
    position = int(position)
    pos[position] = 'X'
    print_board(column, row)
    action = input('flag, enter or cancel?   ')
    if action == 'cancel':
        pos[position] = ' '
        return
    if action == 'flag':
        pos[position] = '🚩'
        flags.append(position)
        print(f'flags = {flags}')
        return
    mine_adjacent = 0
    print(find_adjacent_cells(position))
    adjacent_list = find_adjacent_cells(position)
    for adj_cell in adjacent_list:
        if adj_cell in mine_pos:
            mine_adjacent += 1
    pos[position] = mine_adjacent
    if position in mine_pos:
        print_board(column, row)
        print('you lost!')
        sys.exit()
        return
    steps.append(position)
print_board(column, row)
generate_mine()
print("welcome to the minesweeper!")
print("while not evety time you firstly step on is safe")
while True:
    step()

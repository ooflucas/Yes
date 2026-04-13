import socket
from itertools import combinations
magic_square = [8, 1, 6, 3, 5, 7, 4, 9, 2]
display_board = [str(i) for i in range(9)]
moves = {'X': [], 'O': []}
def get_board_layout():
    return (
        f"\n{display_board[0]} | {display_board[1]} | {display_board[2]}\n"
        f"{display_board[3]} | {display_board[4]} | {display_board[5]}\n"
        f"{display_board[6]} | {display_board[7]} | {display_board[8]}\n"
    )
def check_win(player_char):
    player_moves = moves[player_char]
    if len(player_moves) < 3: return False
    return any(sum(combo) == 15 for combo in combinations(player_moves, 3))
def send_msg(conn, text):
    # Adding \n ensures the client can split "clumped" messages
    conn.sendall((text + "\n").encode())
def get_recv(conn):
    try:
        data = conn.recv(1024).decode().strip()
        return data if data else "QUIT"
    except:
        return "QUIT"
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allows instant restart
server.bind(('0.0.0.0', 12345))
server.listen(2)
print('Server running... Waiting for players.')
conn1, addr1 = server.accept()
send_msg(conn1, "You are Player X. Waiting for Player O...")
print(f"X joined: {addr1}")
conn2, addr2 = server.accept()
send_msg(conn2, "You are Player O. Match starting!")
print(f"O joined: {addr2}")
board = get_board_layout()
for c in [conn1, conn2]:
    send_msg(c, "--- TIC-TAC-TOE ---")
    send_msg(c, board)
game_over = False
for turn in range(9):
    if game_over: break
    p_char = "X" if turn % 2 == 0 else "O"
    curr_conn = conn1 if p_char == "X" else conn2
    other_conn = conn2 if p_char == "X" else conn1
    while True:
        send_msg(curr_conn, f"CHOOSE:Player {p_char}, choose a square (0-8):")
        send_msg(other_conn, f"Wait... Player {p_char} is moving.")
        raw_move = get_recv(curr_conn)
        if raw_move == "QUIT":
            send_msg(other_conn, "Opponent left. Closing.")
            game_over = True
            break
        try:
            move = int(raw_move)
            if 0 <= move <= 8 and display_board[move] not in ['X', 'O']:
                display_board[move] = p_char # Store string "X", not the socket!
                moves[p_char].append(magic_square[move])
                break
            else:
                send_msg(curr_conn, "INVALID:Spot taken or out of range.")
        except ValueError:
            send_msg(curr_conn, "INVALID:Enter a number 0-8.")
    if game_over: break
    board = get_board_layout()
    for c in [conn1, conn2]:
        send_msg(c, board)
    if check_win(p_char):
        for c in [conn1, conn2]:
            send_msg(c, f"GAMEOVER:Player {p_char} wins!")
        game_over = True
        break
else:
    if not game_over:
        for c in [conn1, conn2]:
            send_msg(c, "GAMEOVER:It's a draw!")
print("Closing connections...")
conn1.close()
conn2.close()
server.close()
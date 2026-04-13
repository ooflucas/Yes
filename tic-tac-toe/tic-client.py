import socket
import time
client = socket.socket()
client.connect(('127.0.0.1', 12345))
client.settimeout(0.5) 
while True:
    try:
        data = client.recv(1024).decode()
        if not data: break
        print(data)
        if "CHOOSE:" in data:
            move = input(">>> ")
            client.send(move.encode())
        elif "GAMEOVER:" in data:
            print("Match finished.")
            break
    except socket.timeout:
        continue
    except Exception as e:
        print(f"Error: {e}")
        break
print('match has finished. closing in 5 seconds')
time.sleep(5)
client.close()

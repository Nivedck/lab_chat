import socket
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000

clients = []
names = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# allows quick restart without "address already in use"
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen()

print("Server started...")

def broadcast(message):
    for c in clients:
        try:
            c.sendall(message.encode())
        except:
            if c in clients:
                clients.remove(c)

def handle(client):
    name = names[client]

    while True:
        try:
            msg = client.recv(1024).decode()

            time = datetime.now().strftime("%H:%M")
            formatted = f"[{time}] {msg}"

            print(formatted)
            broadcast(formatted)

        except:
            if client in clients:
                clients.remove(client)

            leave_msg = f"*** {name} left the chat ***"
            print(leave_msg)
            broadcast(leave_msg)

            client.close()
            break

while True:
    client, addr = server.accept()
    print("Connected:", addr)

    name = client.recv(1024).decode()

    clients.append(client)
    names[client] = name

    join_msg = f"*** {name} joined the chat ***"
    print(join_msg)
    broadcast(join_msg)

    thread = threading.Thread(target=handle, args=(client,), daemon=True)
    thread.start()

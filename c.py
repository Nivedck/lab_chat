import socket
import threading

SERVER_IP = input("Enter server IP: ")
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

name = input("Enter your name: ")
client.send(name.encode())

def receive():
    while True:
        try:
            msg = client.recv(1024).decode()
            print(msg)
        except:
            print("Disconnected from server")
            break

def send():
    while True:
        message = input("")
        full = f"{name}: {message}"
        try:
            client.send(full.encode())
        except:
            break

threading.Thread(target=receive, daemon=True).start()
threading.Thread(target=send, daemon=True).start()

# keep program running
while True:
    pass

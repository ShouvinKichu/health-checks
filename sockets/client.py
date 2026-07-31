import socket

HOST = "127.0.0.1"
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

filename = input("Filename: ")
client.sendall(filename.encode())

message = client.recv(1024).decode()
print(message, end="")

substring = input()
client.sendall(substring.encode())

while True:

    data = client.recv(1024)

    if not data:
        break

    print(data.decode(), end="")

client.close()
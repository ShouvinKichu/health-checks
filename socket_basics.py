import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("127.0.0.1",8000))

server.listen()

print("waiting for client")

client_socket, client_address = server.accept()

print(f"client connected to {client_address}")

data = client_socket.recv(1024)

print(data.decode())

client_socket.send(b"Hello client")
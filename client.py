import socket

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(("127.0.0.1",8000))

message = "Hello server"

client.send(message.encode())

reply = client.recv(1024)

print(reply.decode())
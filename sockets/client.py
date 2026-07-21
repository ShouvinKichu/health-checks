import socket

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(("127.0.0.1",8080))

while True:

    message = input("You: ")

    if message.lower() == 'quit':
        break

    client.send(message.encode())

    reply = client.recv(1024).decode()

    print(f"Server: {reply}")

client.close()
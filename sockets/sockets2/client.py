import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1",8000))

while True:

    message = input("YOU: ")

    if message.lower() == 'quit':
        break

    client.send(message.encode())

    response = client.recv(1024).decode()

    print(response)

client.close()
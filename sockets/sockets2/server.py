import socket
import threading

def handle_client(client_socket,client_add):
    while True:
        message = client_socket.recv(1024).decode()

        if not message:
            break

        print(message)

        reply = "Message recieved !!"

        client_socket.send(reply.encode())

    print(f"Server is disconnect to {client_add}")

    client_socket.close()

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(("127.0.0.1",8000))

server.listen()

print("Server is listening....")

while True:
    client_socket, client_add = server.accept()

    print(f"Server is connected to {client_add}")

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket,client_add)
    )

    thread.start()


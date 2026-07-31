import socket
import threading

HOST = "127.0.0.1"
PORT = 5050


def receive_messages(client):

    while True:

        try:

            data = client.recv(1024)

            if not data:
                print("\nServer disconnected")
                break

            print("\n" + data.decode(), end="")

        except OSError:
            break


client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect((HOST, PORT))

username = input("Username: ")

client.sendall(username.encode())


thread = threading.Thread(
    target=receive_messages,
    args=(client,),
    daemon=True
)

thread.start()


while True:

    message = input()

    if message.lower() == "quit":
        break

    client.sendall(message.encode())


client.close()
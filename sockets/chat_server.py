import socket
import threading

HOST = "127.0.0.1"
PORT = 5050

clients = []
lock = threading.Lock()


def broadcast(message, sender):

    with lock:
        current_clients = list(clients)

    for client in current_clients:

        if client != sender:

            try:
                client.sendall(message)

            except OSError:
                pass


def handle_client(conn, addr):

    print("Connected:", addr)

    # First message = username
    data = conn.recv(1024)

    if not data:
        conn.close()
        return

    username = data.decode().strip()

    with lock:
        clients.append(conn)

    print(username, "joined")

    broadcast(
        f"{username} joined the chat\n".encode(),
        conn
    )

    try:

        while True:

            data = conn.recv(1024)

            if not data:
                break

            message = data.decode().strip()

            print(f"{username}: {message}")

            broadcast(
                f"{username}: {message}\n".encode(),
                conn
            )

    finally:

        with lock:
            if conn in clients:
                clients.remove(conn)

        conn.close()

        print(username, "disconnected")

        broadcast(
            f"{username} left the chat\n".encode(),
            conn
        )


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind((HOST, PORT))
server.listen()

print("Chat server listening...")

while True:

    conn, addr = server.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(conn, addr)
    )

    thread.start()
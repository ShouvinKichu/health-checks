import socket
import threading
import sys

HOST = "127.0.0.1"

SERVER_ID = sys.argv[1]
PORT = int(sys.argv[2])


def handle_client(conn):

    try:
        data = conn.recv(1024)

        if not data:
            return

        message = data.decode().strip()

        if message == "Hello":
            response = f"Hello from {SERVER_ID}\n"
        else:
            response = f"{SERVER_ID}: unknown command\n"

        conn.sendall(response.encode())

    finally:
        conn.close()


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

server.bind((HOST, PORT))
server.listen()

print(f"{SERVER_ID} listening on {PORT}")

while True:

    conn, addr = server.accept()

    threading.Thread(
        target=handle_client,
        args=(conn,),
        daemon=True
    ).start()
import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

backends = [
    ("127.0.0.1", 6001),
    ("127.0.0.1", 6002)
]

current = 0

lock = threading.Lock()


def get_backend():

    global current

    with lock:

        backend = backends[current]

        current = (current + 1) % len(backends)

    return backend


def handle_client(client_conn):

    backend_conn = None

    try:
        # Receive request from client
        request = client_conn.recv(1024)

        if not request:
            return

        # Pick backend
        backend_host, backend_port = get_backend()

        print("Forwarding to:", backend_port)

        # LB acts as a CLIENT to backend
        backend_conn = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        backend_conn.connect(
            (backend_host, backend_port)
        )

        # Client -> LB -> Backend
        backend_conn.sendall(request)

        # Backend -> LB
        response = backend_conn.recv(1024)

        # LB -> Client
        client_conn.sendall(response)

    except OSError as e:

        print("Error:", e)

        try:
            client_conn.sendall(
                b"Backend unavailable\n"
            )
        except OSError:
            pass

    finally:

        if backend_conn:
            backend_conn.close()

        client_conn.close()


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

print("Load balancer listening on port 5000")


while True:

    conn, addr = server.accept()

    threading.Thread(
        target=handle_client,
        args=(conn,),
        daemon=True
    ).start()
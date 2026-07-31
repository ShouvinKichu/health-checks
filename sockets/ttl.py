import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 5050

# key -> (value, expiry_time)
store = {}

# Protect shared dictionary
lock = threading.Lock()


def handle_client(conn, addr):
    print("Connected:", addr)

    while True:
        data = conn.recv(1024)

        if not data:
            break

        message = data.decode().strip()

        if not message:
            continue

        print(addr, ":", message)

        parts = message.split()
        command = parts[0].upper()

        # --------------------
        # PUT key value ttl
        # --------------------

        if command == "PUT":

            if len(parts) != 4:
                response = "ERROR Usage: PUT key value ttl"

            else:
                key = parts[1]
                value = parts[2]

                try:
                    ttl = int(parts[3])

                    expiry_time = time.time() + ttl

                    with lock:
                        store[key] = (value, expiry_time)

                    response = "OK"

                except ValueError:
                    response = "ERROR TTL must be integer"

        # --------------------
        # GET key
        # --------------------

        elif command == "GET":

            if len(parts) != 2:
                response = "ERROR Usage: GET key"

            else:
                key = parts[1]

                with lock:

                    if key not in store:

                        response = "NOT_FOUND"

                    else:

                        value, expiry_time = store[key]

                        if time.time() >= expiry_time:

                            del store[key]

                            response = "NOT_FOUND"

                        else:

                            response = value

        # --------------------
        # DELETE key
        # --------------------

        elif command == "DELETE":

            if len(parts) != 2:
                response = "ERROR Usage: DELETE key"

            else:
                key = parts[1]

                with lock:

                    if key in store:

                        del store[key]

                        response = "OK"

                    else:

                        response = "NOT_FOUND"

        # --------------------
        # Unknown command
        # --------------------

        else:
            response = "UNKNOWN_COMMAND"

        conn.sendall((response + "\n").encode())

    conn.close()

    print("Disconnected:", addr)


# ==========================
# SERVER
# ==========================

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind((HOST, PORT))

server.listen()

print(f"KV server listening on {HOST}:{PORT}")

while True:

    conn, addr = server.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(conn, addr)
    )

    thread.start()
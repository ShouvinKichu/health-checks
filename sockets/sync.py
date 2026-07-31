import socket
import threading
import os
import sys
import time
import json
import hashlib

HOST = "127.0.0.1"

CONFIG = {
    "alpha": {
        "port": 5001,
        "peer_port": 5002
    },
    "bravo": {
        "port": 5002,
        "peer_port": 5001
    }
}

POLL_INTERVAL = 1

# Prevent received changes from immediately being sent back.
ignore = {}
ignore_lock = threading.Lock()


# ============================================================
# FILE STATE
# ============================================================

def file_hash(path):
    h = hashlib.sha256()

    try:
        with open(path, "rb") as f:
            while True:
                chunk = f.read(4096)

                if not chunk:
                    break

                h.update(chunk)

        return h.hexdigest()

    except (FileNotFoundError, IsADirectoryError):
        return None


def scan_folder(folder):
    """
    Returns:

    {
        "file.txt": hash,
        "hello.txt": hash
    }
    """

    state = {}

    for name in os.listdir(folder):

        path = os.path.join(folder, name)

        if os.path.isfile(path):
            state[name] = file_hash(path)

    return state


# ============================================================
# NETWORK PROTOCOL
# ============================================================

def recv_exact(sock, size):

    data = b""

    while len(data) < size:

        chunk = sock.recv(size - len(data))

        if not chunk:
            raise ConnectionError("Connection closed")

        data += chunk

    return data


def send_message(event, filename, content=b""):

    header = {
        "event": event,
        "filename": filename,
        "size": len(content)
    }

    header_bytes = json.dumps(header).encode()

    packet = (
        len(header_bytes).to_bytes(4, "big")
        + header_bytes
        + content
    )

    return packet


def receive_message(conn):

    header_size_bytes = recv_exact(conn, 4)

    header_size = int.from_bytes(
        header_size_bytes,
        "big"
    )

    header_bytes = recv_exact(
        conn,
        header_size
    )

    header = json.loads(
        header_bytes.decode()
    )

    content = recv_exact(
        conn,
        header["size"]
    )

    return header, content


# ============================================================
# SEND EVENT TO PEER
# ============================================================

def send_to_peer(peer_port, event, filename, folder):

    content = b""

    if event in ("CREATE", "MODIFY"):

        path = os.path.join(folder, filename)

        try:
            with open(path, "rb") as f:
                content = f.read()

        except FileNotFoundError:
            return

    packet = send_message(
        event,
        filename,
        content
    )

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as sock:

            sock.settimeout(2)

            sock.connect(
                (HOST, peer_port)
            )

            sock.sendall(packet)

        print("SENT:", event, filename)

    except OSError:

        print("Peer unavailable:", event, filename)


# ============================================================
# APPLY RECEIVED EVENT
# ============================================================

def apply_event(folder, header, content):

    event = header["event"]
    filename = header["filename"]

    # Prevent paths like ../../something
    filename = os.path.basename(filename)

    path = os.path.join(
        folder,
        filename
    )

    if event in ("CREATE", "MODIFY"):

        with open(path, "wb") as f:
            f.write(content)

        print("RECEIVED:", event, filename)

        # Remember the resulting state so watcher
        # doesn't immediately send it back.
        with ignore_lock:
            ignore[filename] = file_hash(path)

    elif event == "DELETE":

        try:
            os.remove(path)

        except FileNotFoundError:
            pass

        print("RECEIVED: DELETE", filename)

        with ignore_lock:
            ignore[filename] = None


# ============================================================
# TCP SERVER
# ============================================================

def handle_connection(conn, folder):

    try:

        header, content = receive_message(conn)

        apply_event(
            folder,
            header,
            content
        )

    except Exception as e:
        print("Connection error:", e)

    finally:
        conn.close()


def run_server(folder, port):

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind(
        (HOST, port)
    )

    server.listen()

    print(
        f"Listening on {HOST}:{port}"
    )

    while True:

        conn, addr = server.accept()

        threading.Thread(
            target=handle_connection,
            args=(conn, folder),
            daemon=True
        ).start()


# ============================================================
# DIRECTORY WATCHER
# ============================================================

def watch_folder(folder, peer_port):

    previous = scan_folder(folder)

    while True:

        time.sleep(POLL_INTERVAL)

        current = scan_folder(folder)

        # -------------------------
        # CREATE
        # -------------------------

        for filename in current:

            if filename not in previous:

                with ignore_lock:

                    if (
                        filename in ignore
                        and ignore[filename] == current[filename]
                    ):
                        del ignore[filename]
                        continue

                send_to_peer(
                    peer_port,
                    "CREATE",
                    filename,
                    folder
                )

        # -------------------------
        # MODIFY
        # -------------------------

        for filename in current:

            if (
                filename in previous
                and current[filename] != previous[filename]
            ):

                with ignore_lock:

                    if (
                        filename in ignore
                        and ignore[filename] == current[filename]
                    ):
                        del ignore[filename]
                        continue

                send_to_peer(
                    peer_port,
                    "MODIFY",
                    filename,
                    folder
                )

        # -------------------------
        # DELETE
        # -------------------------

        for filename in previous:

            if filename not in current:

                with ignore_lock:

                    if (
                        filename in ignore
                        and ignore[filename] is None
                    ):
                        del ignore[filename]
                        continue

                send_to_peer(
                    peer_port,
                    "DELETE",
                    filename,
                    folder
                )

        previous = current


# ============================================================
# MAIN
# ============================================================

if len(sys.argv) != 2:

    print(
        "Usage: python3 sync.py alpha|bravo"
    )

    sys.exit(1)


folder = sys.argv[1]


if folder not in CONFIG:

    print(
        "Folder must be alpha or bravo"
    )

    sys.exit(1)


os.makedirs(
    folder,
    exist_ok=True
)


port = CONFIG[folder]["port"]

peer_port = CONFIG[folder]["peer_port"]


print("Folder:", folder)
print("Port:", port)
print("Peer:", peer_port)


threading.Thread(
    target=run_server,
    args=(folder, port),
    daemon=True
).start()


watch_folder(
    folder,
    peer_port
)
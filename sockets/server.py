import socket
import threading



store = {}

def handle_client(conn, addr):
    print(f"server is connected to {addr}")

    while True:
        data = conn.recv(1024)

        if not data:
            break

        message = data.decode().strip()

        print(addr, ":" , message)

        parts = message.split()

        if not parts:
            continue

        command = parts[0].upper()

        #PUT
        if command == "PUT":
            if len(parts) < 3:
                response = "ERR put key value"

            else:
                key = parts[1]

                value = " ".join(parts[2:])

                store[key] = value

                response = "OK"

        #GET
        elif command == "GET":
            if len !=2:
                response = "ERROR: GET key"

            else:
                key = parts[1]

                if key in store:
                    response = store[key]
                else:
                    response = "NOT_FOUND"


        #DEL
        elif command == "DEL":
            if len !=2:
                response = "ERR KEY value"

            else:
                key = parts[1]

                if key in store:
                    del store[key]
                else:
                    response = "NOT_FOUND"

        else:
            response = "UNKOWN_COMMAND"

        conn.sendall((response + "\n").encode())

    conn.close()
    print("Disconnected to", {addr})


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(("127.0.0.1",8080))

server.listen()

print("server is listening..")

while True:

    conn, addr = server.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(conn,addr)
    )

    thread.start()
import socket
import threading

def handle_client(client_socket, client_address):
    while True:

        data = client_socket.recv(1024)

        if not data:
            break

        message = data.decode()

        print(f"{client_address} --> {message}")

        response = "Message recieved!"

        client_socket.send(response.encode())

    print(f"Connection is closed for {client_address}")

    client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("127.0.0.1",8080))

server.listen()


while True:

    client_socket, client_address = server.accept()

    print(f"client is connected to {client_address}")

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket,client_address)
    )
    
    thread.start()
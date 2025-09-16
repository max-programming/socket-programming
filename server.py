import socket
import threading
from faker import Faker

fake = Faker()
clients: dict[socket.socket, str] = {}


def broadcast(message: str, sender_socket: socket.socket | None):
    for client in list(clients.keys()):
        if client != sender_socket:
            try:
                client.sendall(message.encode())
            except Exception:
                client.close()
                del clients[client]


def handle_client(client_socket: socket.socket, client_addr: str):
    username = fake.user_name()
    clients[client_socket] = username

    print(f"[+] {username} connected from {client_addr}")
    broadcast(f"{username} joined the chat", sender_socket=None)

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            msg = data.decode().strip()
            print(f"{username}: {msg}")
            broadcast(f"{username}: {msg}", sender_socket=client_socket)
    except Exception as e:
        print(f"[!] Error with {username}: {e}")
    finally:
        print(f"[-] {username} disconnected")
        broadcast(f"[-] {username} left the chat.", sender_socket=None)
        client_socket.close()
        del clients[client_socket]


def main():
    HOST = "127.0.0.1"
    PORT = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, client_addr = server_socket.accept()
        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_addr),
        )
        thread.start()


if __name__ == "__main__":
    main()

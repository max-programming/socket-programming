import socket
import threading


def receive_messages(client_socket: socket.socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(message.decode().strip())
        except Exception:
            print("Disconnected from server")
            break


def send_messages(client_socket: socket.socket):
    while True:
        try:
            msg = input("")
            if msg.lower() == "quit":
                client_socket.close()
                break
            client_socket.sendall(msg.encode())
        except Exception:
            break


def main():
    HOST = "127.0.0.1"
    PORT = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print(f"Connected to chat server {HOST}:{PORT}")
    print("Type messages and press Enter. Type 'quit' to exit.\n")

    threading.Thread(
        target=receive_messages, args=(client_socket,), daemon=True
    ).start()
    send_messages(client_socket)


if __name__ == "__main__":
    main()

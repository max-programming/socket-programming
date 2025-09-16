# Socket Programming Client Implementation Explanation

This document explains the client-side implementation that connects to the multi-client chat server.

## 1. Imports and Threading Setup

```python
import socket
import threading
```

The client uses the same `socket` and `threading` modules as the server, but for different purposes. Here, threading enables **simultaneous sending and receiving** of messages - the client can listen for incoming messages while the user types new ones, creating a smooth chat experience.

## 2. Receive Messages Function

```python
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
```

This function runs in a **background thread** and continuously listens for messages from the server. It receives data in 1024-byte chunks, decodes the bytes to strings, and immediately prints them to the console. When the server closes the connection (empty message) or a network error occurs, the loop breaks and the thread terminates.

The key difference from the server's receive logic is that the client simply displays messages rather than processing or redistributing them.

## 3. Send Messages Function

```python
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
```

This function handles user input and message transmission. It runs in the **main thread** and blocks on `input()` waiting for the user to type messages. When the user types "quit", it closes the connection and exits the loop.

Unlike the server which broadcasts messages to multiple clients, the client simply sends each message directly to the server, which then handles the broadcasting logic.

## 4. Main Function

```python
def main():
    HOST = "127.0.0.1"
    PORT = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print(f"Connected to chat server {HOST}:{PORT}")
    print("Type messages and press Enter. Type 'quit' to exit.\n")

    thread = threading.Thread(
        target=receive_messages,
        args=(client_socket,),
        daemon=True,
    )
    thread.start()
    send_messages(client_socket)
```

The client creates a TCP socket and **connects** to the server (rather than binding and listening like the server does). Once connected, it starts two concurrent operations:

1. **Background receiving thread**: Marked as `daemon=True`, meaning it will automatically terminate when the main program exits
2. **Main sending thread**: Runs `send_messages()` in the current thread, handling user input

**Why Threading is Essential for the Client**: Without threading, the client would have to alternate between checking for new messages and waiting for user input. This would mean:

- Messages from other users might be delayed or missed
- Poor user experience with laggy message delivery
- The interface would feel unresponsive

With threading, the client can **simultaneously** display incoming messages while allowing the user to type new ones, creating a real-time chat experience. The daemon thread ensures clean program termination when the user quits.

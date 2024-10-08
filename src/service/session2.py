import socket
import threading
import time


class Session:
    def __init__(self, server_address: tuple[str, int]) -> None:
        self.session_socket: socket.socket = None
        self.connect_to_server(server_address)

    def connect_to_server(self, server_address: tuple[str, int]) -> None:
        while True:
            try:
                self.session_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.session_socket.connect((server_address[0], server_address[1]))
                print(f"Connected with server {server_address[0]}:{server_address[1]}")

                self.session_socket.send(b"Session")

                threading.Thread(target=self.write_message).start()
                threading.Thread(target=self.receive_message).start()
                break
            except:
                print("Failed to connect to server. Reconnecting...")
                time.sleep(3)

    def write_message(self) -> None:
        while True:
            try:
                message: str = input("")
                if not message:
                    raise ConnectionResetError("Session input closed")

                self.session_socket.send(message.encode())
            except Exception as e:
                print(f"An error occurred with writing message: ({e})")
                self.session_socket.close()
                break

    def receive_message(self) -> None:
        while True:
            try:
                message: str = self.session_socket.recv(1024).decode()
                if not message:
                    raise ConnectionResetError("Server disconnected")

                print(f"Guest: {message}")
            except:
                print("Problem occurred with receiving message from server")
                self.session_socket.close()
                break

if __name__ == "__main__":
    session = Session("localhost", 55556)

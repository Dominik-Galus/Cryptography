import socket
import threading


class Server:
    def __init__(self, address: tuple[str, int]) -> None:
        self.host: str
        self.port: int
        self.host, self.port = address
        self.server_connection: socket.socket = None
        self.server_socket: socket.socket = None
        self.start_server()
        self.sessions: list[socket.socket] = []

    def start_server(self) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server is listening on {self.host}:{self.port}")

    def connection_handler(self, address: tuple[str, int]) -> None:
        connecting_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            print(f"Trying to connect to {address[0]}:{address[1]}...")
            connecting_socket.connect((address[0], address[1]))
            self.server_connection = connecting_socket
            self.server_connection.sendall(f"{self.port}".encode())
            threading.Thread(target=self.receive_data_from_server).start()
            print("Connected with server")

            while True:
                sc, sockname = self.server_socket.accept()
                response = sc.recv(1024).decode()
                if response == "Session":
                    print(f"Connected with session at {sockname}")
                    self.sessions.append(sc)
                    threading.Thread(target=self.receive_data_from_session, args=(sc,)).start()

        except:
            print(f"Failed to connect to: {address[0]}:{address[1]}...")
            print("Waiting for server to connect...")

            while True:
                sc, sockname = self.server_socket.accept()
                response = sc.recv(1024).decode()
                if response == str(address[1]):
                    self.server_connection = sc
                    print("Connected with the server")

                    threading.Thread(target=self.receive_data_from_server).start()
                else:
                    print(f"Connected with session at {sockname}")
                    self.sessions.append(sc)

                    threading.Thread(target=self.receive_data_from_session, args=(sc,)).start()

    def receive_data_from_session(self, session: socket.socket) -> None:
        while True:
            try:
                message = session.recv(1024).decode()
                if not message:
                    raise ConnectionResetError("Session disconnected")
                if self.server_connection:
                    self.forward_data_to_server(message)
            except Exception as e:
                print(f"An error occurred while receiving data from session: ({e})")
                self.sessions.remove(session)
                session.close()
                break

    def forward_data_to_server(self, message) -> None:
        try:
            self.server_connection.send(message.encode())
            print(f"Forwarded message to connected server: {message}")
        except Exception as e:
            print(f"An error occurred forwarding a data to server: ({e})")

    def receive_data_from_server(self) -> None:
        while True:
            try:
                message = self.server_connection.recv(1024).decode()
                if message:
                    print(f"Received from server: {message}")
                    self.broadcast_to_sessions(message, sender_session = None)
            except Exception as e:
                print(f"An error occurred while receiving data from server: ({e})")
                self.server_connection.close()
                break

    def broadcast_to_sessions(self, message: str, sender_session: socket.socket) -> None:
        for session in self.sessions:
            if session != sender_session:
                try:
                    session.send(message.encode())
                except Exception as e:
                    print(f"An error occurred while broadcasting to sessions: ({e})")
                    self.sessions.remove(session)
                    session.close()

    def stop_server(self) -> None:
        self.server_socket.close()
        if self.server_connection:
            self.server_connection.close()

if __name__ == "__main__":
    server = Server(("localhost", 55556))
    try:
        server.connection_handler(("localhost", 55555))
    except Exception as e:
        print(f"Server stopped: {e}")
        server.stop_server()

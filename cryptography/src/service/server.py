import pathlib
import socket
import threading

import numpy as np

from cryptography.src.keys.asymmetric.asymmetric import Asymmetric
from cryptography.src.keys.factories.asymmetrickeyfactory import AsymmetricKeyFactory
from cryptography.src.keys.factories.symmetrickeyfactory import SymmetricKeyFactory
from cryptography.src.keys.symmetric.symmetric import Symmetric


class Server:
    def __init__(
        self,
        address: tuple[str, int],
        asymmetric_key_type: str,
        asymmetric_bits: int,
        symmetric_key_type: str,
        symmetric_bits: int,
        key_file_index: str,
    ) -> None:
        self.host: str
        self.port: int
        self.host, self.port = address
        self.server_connection: socket.socket = None
        self.server_socket: socket.socket = None
        self.start_server()
        self.sessions: list[socket.socket] = []

        self.asymmetric_key_type = asymmetric_key_type
        self.asymmetric_bits = asymmetric_bits
        self.symmetric_key_type = symmetric_key_type
        self.symmetric_bits = symmetric_bits

        if key_file_index:
            self.load_keys(key_file_index)
        else:
            self.generate_asymmetric_keys()

    def generate_asymmetric_keys(self) -> None:
        asymmetric: Asymmetric = AsymmetricKeyFactory.create_key(
            self.asymmetric_key_type,
            self.asymmetric_bits,
        )
        self.asymmetric_public_key: tuple[int, int] = asymmetric.public_key
        self.asymmetric_private_key: tuple[int, int] = asymmetric.private_key

    def generate_symmetric_key(self) -> np.ndarray:
        symmetric: Symmetric = SymmetricKeyFactory.create_key(
            self.symmetric_key_type,
            self.symmetric_bits,
            None,
        )
        return symmetric.key

    def load_keys(self, key_file_number: str) -> None:
        asymmetric_key: Asymmetric = AsymmetricKeyFactory.get_key(
            self.asymmetric_key_type,
        )

        if not (
            path_to_public := pathlib.Path(
                f"cryptography/src/data/asymmetric_public_key_{key_file_number}.txt"
            )
        ).exists():
            raise FileNotFoundError("Public key file not found")
        if not (
            path_to_private := pathlib.Path(
                f"cryptography/src/data/asymmetric_private_key_{key_file_number}.txt"
            )
        ).exists():
            raise FileNotFoundError("Private key file not found")

        with open(path_to_public) as key_file:
            self.asymmetric_public_key = asymmetric_key.load_from_file(
                content=key_file.read(),
            )

        with open(path_to_private) as key_file:
            self.asymmetric_private_key = asymmetric_key.load_from_file(
                content=key_file.read(),
            )

    def start_server(self) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server is listening on {self.host}:{self.port}")

    def connection_handler(self, address: tuple[str, int]) -> None:
        connecting_socket: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )

        try:
            print(f"Trying to connect to {address[0]}:{address[1]}...")
            connecting_socket.connect((address[0], address[1]))

            self.server_connection = connecting_socket
            self.server_connection.sendall(f"{self.port}-".encode())
            self.send_asymmetric_public_key_to_server()
            key: str = self.server_connection.recv(self.asymmetric_bits * 16).decode()

            threading.Thread(target=self.receive_data_from_server).start()
            print("Connected with server")

            while True:
                sc, sockname = self.server_socket.accept()

                response = sc.recv(1024).decode()

                if response == "Session":
                    print(f"Connected with session at {sockname}")
                    self.sessions.append(sc)
                    self.send_decrypted_symmetric_data_to_session(key, sc)
                    threading.Thread(
                        target=self.receive_data_from_session, args=(sc,)
                    ).start()

        except Exception as e:
            symmetric_key: np.ndarray = self.generate_symmetric_key()
            print(f"Failed to connect to: {address[0]}:{address[1]} ({e})")
            print("Waiting for server to connect...")

            while True:
                sc, sockname = self.server_socket.accept()
                received = sc.recv(1024).decode()
                response: list[str] = received.split("-")
                if response[0] == str(address[1]):
                    self.server_connection = sc
                    print("Connected with the server")
                    self.send_encrypted_symmetric_key_to_server(
                        symmetric_key, response[1]
                    )
                    threading.Thread(target=self.receive_data_from_server).start()
                else:
                    print(f"Connected with session at {sockname}")
                    self.sessions.append(sc)
                    self.send_symmetric_data_to_session(symmetric_key, sc)
                    threading.Thread(
                        target=self.receive_data_from_session, args=(sc,)
                    ).start()

    def send_asymmetric_public_key_to_server(self) -> None:
        asymmetric_public_key = " ".join(
            [
                str(self.asymmetric_public_key[0]),
                str(self.asymmetric_public_key[1]),
                self.asymmetric_key_type,
            ]
        )
        self.server_connection.sendall(asymmetric_public_key.encode())

    def send_encrypted_symmetric_key_to_server(
        self, symmetric_key: np.ndarray, asymmetric_public_key: str
    ) -> None:
        asymmetric_public_key: list[str] = asymmetric_public_key.split(" ")
        e: int = int(asymmetric_public_key[0])
        n: int = int(asymmetric_public_key[1])
        asymmetric_key_type = asymmetric_public_key[2]
        encrypted_symmetric_key: str = self.encrypt_symmetric_key(
            symmetric_key, (e, n), asymmetric_key_type
        )

        self.server_connection.sendall(encrypted_symmetric_key.encode())

    def encrypt_symmetric_key(
        self,
        symmetric_key: np.ndarray,
        asymmetric_public_key: tuple[int, int],
        asymmetric_key_type,
    ) -> str:
        other_public_asymmetric_key, other_n = asymmetric_public_key

        other_asymmetric_key: Asymmetric = AsymmetricKeyFactory.get_key(
            asymmetric_key_type
        )
        encrypted_symmetric_key: list[str] = [
            other_asymmetric_key.encrypt_with_known_key(
                str(byte), (other_public_asymmetric_key, other_n)
            )
            for byte in symmetric_key.flatten()
        ]

        encrypted_symmetric_key: bytes = " ".join(encrypted_symmetric_key)
        return encrypted_symmetric_key

    def receive_data_from_session(self, session: socket.socket) -> None:
        while True:
            try:
                message = session.recv(self.asymmetric_bits * 16).decode()
                if not message:
                    raise ConnectionResetError("Session disconnected")
                if self.server_connection:
                    self.forward_data_to_server(message)
            except Exception as e:
                print(f"An error occurred while receiving data from session: ({e})")
                self.sessions.remove(session)
                session.close()
                break

    def send_decrypted_symmetric_data_to_session(
        self, encrypted_symmetric_key: str, session: socket.socket
    ) -> None:
        asymmetric_key: Asymmetric = AsymmetricKeyFactory.get_key(
            self.asymmetric_key_type
        )

        encrypted_symmetric_key: list[str] = encrypted_symmetric_key.split(" ")
        symmetric_key: list[str] = [
            asymmetric_key.decrypt_with_known_key(char, self.asymmetric_private_key)
            for char in encrypted_symmetric_key
        ]
        symmetric_key: str = " ".join(symmetric_key)

        symmetric_data: str = "-".join(
            [symmetric_key, self.symmetric_key_type, str(self.symmetric_bits)]
        )

        session.send(symmetric_data.encode())

    def send_symmetric_data_to_session(
        self, symmetric_key: np.ndarray, session: socket.socket
    ) -> None:
        symmetric_key: str = " ".join([str(byte) for byte in symmetric_key.flatten()])
        symmetric_data: str = "-".join(
            [symmetric_key, self.symmetric_key_type, str(self.symmetric_bits)]
        )

        session.send(symmetric_data.encode())

    def forward_data_to_server(self, message) -> None:
        try:
            self.server_connection.send(message.encode())
            print(f"Forwarded message to connected server: {message}")
        except Exception as e:
            print(f"An error occurred forwarding a data to server: ({e})")

    def receive_data_from_server(self) -> None:
        while True:
            try:
                message = self.server_connection.recv(
                    self.asymmetric_bits * 16
                ).decode()
                if message:
                    print(f"Received from server: {message}")
                    self.broadcast_to_sessions(message, sender_session=None)
            except Exception as e:
                print(f"An error occurred while receiving data from server: ({e})")
                self.server_connection.close()
                break

    def broadcast_to_sessions(
        self, message: str, sender_session: socket.socket
    ) -> None:
        for session in self.sessions:
            if session != sender_session:
                try:
                    session.send(message.encode())
                except Exception as e:
                    print(f"An error occurred while broadcasting to sessions: ({e})")
                    self.sessions.remove(session)
                    session.close()


if __name__ == "__main__":
    server = Server(
        address=("localhost", 55556),
        asymmetric_key_type="RSA",
        asymmetric_bits=1024,
        symmetric_key_type="AES",
        symmetric_bits=128,
        key_file_index="2",
    )
    server.connection_handler(("localhost", 55555))

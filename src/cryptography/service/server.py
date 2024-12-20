import json
import pathlib
import socket
import threading
from typing import TYPE_CHECKING

import numpy as np

import cryptography.configs.connection_config as conn
from cryptography.configs.logging_config import setup_logging
from cryptography.keys.factories.asymmetrickeyfactory import AsymmetricKeyFactory
from cryptography.keys.factories.symmetrickeyfactory import SymmetricKeyFactory

if TYPE_CHECKING:
    import logging

    from cryptography.keys.asymmetric.asymmetric import Asymmetric
    from cryptography.keys.symmetric.symmetric import Symmetric

DEFAULT_SERVER_ADDRESS: tuple[str, int] = ("localhost", 55560)

class Server:
    def __init__(
        self,
        address: tuple[str, int] | None,
        asymmetric_key_data: tuple[str, int],
        symmetric_key_data: tuple[str, int],
        path_to_key: str | None,
        logging_level: str = "INFO",
    ) -> None:
        logger_name: str = f"{__name__}.{__class__.__name__}"
        self.logger: logging.Logger = setup_logging(logger_name, log_level=logging_level)
        self.host: str
        self.port: int

        if address is None:
            address = DEFAULT_SERVER_ADDRESS

        self.host, self.port = address
        self.server_connection: socket.socket = None
        self.server_socket: socket.socket = None
        self.start_server()
        self.sessions: list[socket.socket] = []

        asymmetric_key_type, asymmetric_bits = asymmetric_key_data
        symmetric_key_type, symmetric_bits = symmetric_key_data

        self.asymmetric_key_type = asymmetric_key_type
        self.asymmetric_bits = asymmetric_bits
        self.symmetric_key_type = symmetric_key_type
        self.symmetric_bits = symmetric_bits

        if path_to_key:
            self.load_keys(path_to_key)
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

    def load_keys(self, path_to_key: str) -> None:
        asymmetric_key: Asymmetric = AsymmetricKeyFactory.get_key(
            self.asymmetric_key_type,
        )
        if path_to_key.endswith("/"):
            path_to_key = path_to_key[:-1]
        if not (
            path_to_public := pathlib.Path(
            f"{path_to_key}/public_key.txt",
            )
        ).exists():
            msg: str = "Public key file not found"
            raise FileNotFoundError(msg)
        if not (
            path_to_private := pathlib.Path(
                f"{path_to_key}/private_key.txt",
            )
        ).exists():
            msg: str = "Private key file not found"
            raise FileNotFoundError(msg)

        with pathlib.Path.open(path_to_public) as key_file:
            self.asymmetric_public_key = asymmetric_key.load_from_file(
                content=key_file.read(),
            )

        with pathlib.Path.open(path_to_private) as key_file:
            self.asymmetric_private_key = asymmetric_key.load_from_file(
                content=key_file.read(),
            )

    def start_server(self) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.logger.info("Server is listening on %s:%s", self.host, self.port)

    def connection_handler(self, address: tuple[str, int]) -> None:
        connecting_socket: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM,
        )

        try:
            self.logger.info("Trying to connect to %s:%s...", address[0], address[1])
            connecting_socket.connect((address[0], address[1]))

            self.server_connection = connecting_socket
            self.send_asymmetric_public_key_to_server()
            key: str = self.server_connection.recv(self.asymmetric_bits * 16).decode()

            threading.Thread(target=self.receive_data_from_server).start()
            self.logger.info("Connected with server")

            while True:
                sc, sockname = self.server_socket.accept()

                response = sc.recv(1024).decode()

                if response == conn.SESSION_MESSAGE:
                    self.logger.info("Connected with session at %s", sockname)
                    self.sessions.append(sc)
                    self.send_decrypted_symmetric_data_to_session(key, sc)
                    threading.Thread(
                        target=self.receive_data_from_session, args=(sc,),
                    ).start()

        except ConnectionRefusedError:
            symmetric_key: np.ndarray = self.generate_symmetric_key()
            self.logger.info("Failed to connect to: %s:%s", address[0], address[1])
            self.logger.info("Waiting for server to connect...")

            while True:
                sc, sockname = self.server_socket.accept()
                response: list[str] = sc.recv(1024).decode()
                if response == conn.SESSION_MESSAGE:
                    self.logger.info("Connected with session at %s", sockname)
                    self.sessions.append(sc)
                    self.send_symmetric_data_to_session(symmetric_key, sc)
                    threading.Thread(
                        target=self.receive_data_from_session, args=(sc,),
                    ).start()
                else:
                    self.server_connection = sc
                    response = json.loads(response)
                    self.logger.info("Connected with the server")
                    self.send_encrypted_symmetric_key_to_server(
                        symmetric_key, response,
                    )
                    threading.Thread(target=self.receive_data_from_server).start()

    def send_asymmetric_public_key_to_server(self) -> None:
        asymmetric_public_key: list[str] = [
            str(self.asymmetric_public_key[0]),
            str(self.asymmetric_public_key[1]),
        ]
        data: dict = {
            conn.SERVER_MESSAGE: f"{self.port}",
            conn.ASYMMETRIC_KEY_TYPE_FIELD_NAME: self.asymmetric_key_type,
            conn.ASYMMETRIC_PUBLIC_KEY_FIELD_NAME: asymmetric_public_key,
            }
        self.server_connection.sendall(json.dumps(data).encode())

    def send_encrypted_symmetric_key_to_server(
        self, symmetric_key: np.ndarray, data: dict[str, str | list[str]],
    ) -> None:
        asymmetric_public_key: list[str] = data[conn.ASYMMETRIC_PUBLIC_KEY_FIELD_NAME]
        e: int = int(asymmetric_public_key[0])
        n: int = int(asymmetric_public_key[1])
        asymmetric_key_type = data[conn.ASYMMETRIC_KEY_TYPE_FIELD_NAME]
        encrypted_symmetric_key: str = self.encrypt_symmetric_key(
            symmetric_key, (e, n), asymmetric_key_type,
        )

        self.server_connection.sendall(encrypted_symmetric_key.encode())

    def encrypt_symmetric_key(
        self,
        symmetric_key: np.ndarray,
        asymmetric_public_key: tuple[int, int],
        asymmetric_key_type: str,
    ) -> str:
        other_public_asymmetric_key, other_n = asymmetric_public_key

        other_asymmetric_key: Asymmetric = AsymmetricKeyFactory.get_key(
            asymmetric_key_type,
        )
        encrypted_symmetric_key: list[str] = [
            other_asymmetric_key.encrypt_with_known_key(
                str(byte), (other_public_asymmetric_key, other_n),
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
                    msg: str = "Session disconnected"
                    raise ConnectionRefusedError(msg)
                if self.server_connection:
                    self.forward_data_to_server(message)
            except Exception:
                self.logger.exception("An error occurred while receiving data from session")
                self.sessions.remove(session)
                session.close()
                break

    def send_decrypted_symmetric_data_to_session(
        self, encrypted_symmetric_key: str, session: socket.socket,
    ) -> None:
        asymmetric_key: Asymmetric = AsymmetricKeyFactory.get_key(
            self.asymmetric_key_type,
        )

        encrypted_symmetric_key: list[str] = encrypted_symmetric_key.split(" ")
        symmetric_key: list[str] = [
            asymmetric_key.decrypt_with_known_key(char, self.asymmetric_private_key)
            for char in encrypted_symmetric_key
        ]
        symmetric_key: str = " ".join(symmetric_key)

        symmetric_data: str = "-".join(
            [symmetric_key, self.symmetric_key_type, str(self.symmetric_bits)],
        )

        session.send(symmetric_data.encode())

    def send_symmetric_data_to_session(
        self, symmetric_key: np.ndarray, session: socket.socket,
    ) -> None:
        symmetric_key: str = " ".join([str(byte) for byte in symmetric_key.flatten()])
        symmetric_data: str = "-".join(
            [symmetric_key, self.symmetric_key_type, str(self.symmetric_bits)],
        )

        session.send(symmetric_data.encode())

    def forward_data_to_server(self, message: str) -> None:
        try:
            self.server_connection.send(message.encode())
            self.logger.info("Forwarded message to connected server: %s", message)
        except Exception:
            self.logger.exception("An error occurred forwarding a data to server")

    def receive_data_from_server(self) -> None:
        while True:
            try:
                message = self.server_connection.recv(
                    self.asymmetric_bits * 16,
                ).decode()
                if message:
                    self.logger.info("Received from server: %s", message)
                    self.broadcast_to_sessions(message, sender_session=None)
            except Exception as e:
                self.logger.exception("An error occurred while receiving data from server: %s", exc_info=e)
                self.server_connection.close()
                break

    def broadcast_to_sessions(
        self, message: str, sender_session: socket.socket,
    ) -> None:
        for session in self.sessions:
            if session != sender_session:
                try:
                    session.send(message.encode())
                except Exception as e:
                    self.logger.exception("An error occurred while broadcasting to sessions: %s", exc_info=e)
                    self.sessions.remove(session)
                    session.close()

if __name__ == "__main__":
    Server(None, None, None)

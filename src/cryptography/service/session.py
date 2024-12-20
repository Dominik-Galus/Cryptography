import socket
import threading
import time
from typing import TYPE_CHECKING

from cryptography.configs.connection_config import SESSION_MESSAGE
from cryptography.configs.logging_config import setup_logging
from cryptography.keys.factories.symmetrickeyfactory import SymmetricKeyFactory

if TYPE_CHECKING:
    import logging

    from cryptography.keys.symmetric.symmetric import Symmetric

class Session:
    def __init__(self, server_address: tuple[str, int], logging_config: str = "INFO") -> None:
        logger_name: str = f"{__name__}.{__class__.__name__}"
        self.logger: logging.Logger = setup_logging(logger_name, logging_config)
        self.session_socket: socket.socket = None
        self.symmetric_key: list[str] = None
        self.bits: int = None
        self.symmetric_type: str = None
        self.connect_to_server(server_address)

    def connect_to_server(self, server_address: tuple[str, int]) -> None:
        while True:
            try:
                self.session_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.session_socket.connect((server_address[0], server_address[1]))
                self.logger.info("Connected with server %s:%s",server_address[0],server_address[1])

                self.session_socket.send(SESSION_MESSAGE.encode())

                self.retrieve_key()

                threading.Thread(target=self.write_message).start()
                threading.Thread(target=self.receive_message).start()
                break
            except Exception:
                self.logger.info("Failed to connect to server. Reconnecting...")
                time.sleep(3)

    def retrieve_key(self) -> None:
        symmetric_data: str = self.session_socket.recv(20000).decode()

        symmetric_data: list[str] = symmetric_data.split("-")
        key: str = symmetric_data[0]
        self.symmetric_type: str = symmetric_data[1]
        self.bits: int = int(symmetric_data[2])

        self.symmetric_key: list[str] = key.split(" ")

    def encrypt_data(self, data: str) -> str:
        symmetric_key: Symmetric = SymmetricKeyFactory.create_key(
            key_type=self.symmetric_type, bits=self.bits, key=self.symmetric_key,
        )
        return symmetric_key.encrypt(data)

    def decrypt_data(self, data: str) -> str:
        symmetric_key: Symmetric = SymmetricKeyFactory.create_key(
            key_type=self.symmetric_type, bits=self.bits, key=self.symmetric_key,
        )
        return symmetric_key.decrypt(data)

    def write_message(self) -> None:
        while True:
            try:
                message: str = input("")
                message = self.encrypt_data(message)
                if not message:
                    msg: str = "Session input closed"
                    raise ConnectionResetError(msg)

                self.session_socket.send(message.encode())
            except Exception as e:
                self.logger.exception("An error occurred with writing message", exc_info=e)
                self.session_socket.close()
                break

    def receive_message(self) -> None:
        while True:
            try:
                message: str = self.session_socket.recv(20000).decode()
                message = self.decrypt_data(message)
                if not message:
                    msg: str = "Server disconnected"
                    raise ConnectionResetError(msg)

                self.logger.info("Guest: %s", message)
            except:
                self.logger.info("Problem occurred with receiving message from server")
                self.session_socket.close()
                break


if __name__ == "__main__":
    session = Session((None, None))

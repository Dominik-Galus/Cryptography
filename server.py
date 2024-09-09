from typing import Self

import numpy as np

from asymmetric import Asymmetric
from asymmetrickeyfactory import AsymmetricKeyFactory
from session import Session
from symmetric import Symmetric
from symmetrickeyfactory import SymmetricKeyFactory


class Server:
    def __init__(
        self, asymmetric_key_type: str,
        asymmetric_bits: int, symmetric_key_type: str,
        symmetric_bits: int, key_file_index: str | None = None,
        ) -> None:
        self.asymmetric_key_type: str = asymmetric_key_type
        self.symmetric_key_type: str = symmetric_key_type
        self.asymmetric_bits: int = asymmetric_bits
        self.symmetric_bits: int = symmetric_bits
        self.sessions: dict[int, "Session"] = {}
        
        if key_file_index is None:
            self.generate_asymmetric_keys()
        else:
            self.load_keys(key_file_index)

    def generate_asymmetric_keys(self) -> None:
        asymmetric: Asymmetric = AsymmetricKeyFactory.create_key(self.asymmetric_key_type, self.asymmetric_bits)
        self.asymmetric_public_key = asymmetric.public_key
        self.asymmetric_private_key = asymmetric.private_key

    def generate_symmetric_key(self) -> np.ndarray:
        symmetric: Symmetric = SymmetricKeyFactory.create_key(self.symmetric_key_type, self.symmetric_bits, None)
        return symmetric.key

    def add_session(self, session: "Session") -> None:
        self.sessions[session.id] = session

    def exchange_key(self, other_server: Self) -> list[int]:
        symmetric_key = self.generate_symmetric_key()
        
        other_asymmetric_key: Asymmetric = AsymmetricKeyFactory.get_key(other_server.asymmetric_key_type)

        encrypted_symmetric_key: list[int] = [
            other_asymmetric_key.encrypt_with_known_key(str(byte), other_server.asymmetric_public_key)
            for byte in symmetric_key.flatten()
        ]

        session = Session(self.symmetric_key_type, symmetric_key, self.symmetric_bits, self.asymmetric_public_key)
        self.add_session(session)

        return encrypted_symmetric_key

    def load_keys(self, key_file_number: str) -> None:
        asymmetric_key: Asymmetric = AsymmetricKeyFactory.get_key(self.asymmetric_key_type)
        with open(f"asymmetric_public_key_{key_file_number}.txt", "r") as key_file:
            self.asymmetric_public_key = asymmetric_key.load_from_file(content=key_file.read())

        with open(f"asymmetric_private_key_{key_file_number}.txt", "r") as key_file:
            self.asymmetric_private_key = asymmetric_key.load_from_file(content=key_file.read())

    def retrieve_key(self, encrypted_symmetric_key: list[int]) -> np.ndarray:
        if self.asymmetric_private_key == None:
            self.generate_asymmetric_keys()
            
        asymmetric_key: Asymmetric = AsymmetricKeyFactory.get_key(self.asymmetric_key_type)

        decrypted_integers: list[int] = asymmetric_key.decrypt_with_known_key(
            encrypted_symmetric_key, self.asymmetric_private_key
        )

        symmetric_key = np.array(decrypted_integers, dtype=np.uint8).reshape(4, 4)

        session = Session(self.symmetric_key_type, symmetric_key, self.symmetric_bits, self.asymmetric_public_key)
        self.add_session(session)

        return symmetric_key


if __name__ == "__main__":
    server1 = Server(
        asymmetric_key_type="RSA",
        asymmetric_bits=1024,
        symmetric_key_type="AES",
        symmetric_bits=128,
        key_file_index="1"
        )
    server2 = Server(
        asymmetric_key_type="RSA",
        asymmetric_bits=1024,
        symmetric_key_type="AES",
        symmetric_bits=128,
        key_file_index="2"
        )

    encrypted_symmetric_key = server1.exchange_key(server2)
    decrypted_symmetric_key = server2.retrieve_key(encrypted_symmetric_key)

    session_server1 = list(server1.sessions.values())[0]
    session_server2 = list(server2.sessions.values())[0]

    encrypted = session_server1.encrypt_data("Secret message")
    decrypted = session_server2.decrypt_data(encrypted)

    assert decrypted == "Secret message"

    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)
    print("******************************************************************")

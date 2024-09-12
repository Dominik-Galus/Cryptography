from typing import Self

import numpy as np

from src.keys.asymmetric.asymmetric import Asymmetric
from src.keys.factories.asymmetrickeyfactory import AsymmetricKeyFactory
from src.service.session import Session
from src.keys.symmetric.symmetric import Symmetric
from src.keys.factories.symmetrickeyfactory import SymmetricKeyFactory


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

        encrypted_symmetric_key: list[str] = [
            other_asymmetric_key.encrypt_with_known_key(str(byte), other_server.asymmetric_public_key)
            for byte in symmetric_key.flatten()
        ]

        session = Session(self.symmetric_key_type, symmetric_key, self.symmetric_bits, self.asymmetric_public_key)
        self.add_session(session)

        return encrypted_symmetric_key

    def load_keys(self, key_file_number: str) -> None:
        asymmetric_key: Asymmetric = AsymmetricKeyFactory.get_key(self.asymmetric_key_type)
        with open(f"src/data/asymmetric_public_key_{key_file_number}.txt", "r") as key_file:
            self.asymmetric_public_key = asymmetric_key.load_from_file(content=key_file.read())

        with open(f"src/data/asymmetric_private_key_{key_file_number}.txt", "r") as key_file:
            self.asymmetric_private_key = asymmetric_key.load_from_file(content=key_file.read())

    def retrieve_key(self, encrypted_symmetric_key: list[int]) -> np.ndarray:    
        asymmetric_key: Asymmetric = AsymmetricKeyFactory.get_key(self.asymmetric_key_type)

        symmetric_key: list[str] = [asymmetric_key.decrypt_with_known_key(
            char, self.asymmetric_private_key
        ) for char in encrypted_symmetric_key]
        
        session = Session(self.symmetric_key_type, symmetric_key, self.symmetric_bits, self.asymmetric_public_key)
        self.add_session(session)

        return symmetric_key


if __name__ == "__main__":
    Server(None, None, None, None, None)

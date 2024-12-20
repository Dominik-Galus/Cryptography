from typing import ClassVar

import numpy as np

from cryptography.keys.factories.keyfactory import KeyFactory
from cryptography.keys.symmetric.aes import AES
from cryptography.keys.symmetric.symmetric import Symmetric


class SymmetricKeyFactory(KeyFactory):

    key_type_map: ClassVar[dict[str, type[Symmetric]]] = {"AES": AES}

    @staticmethod
    def create_key(key_type: str, bits: int, key: np.ndarray | list[str]=None) -> Symmetric:
        if key_type in SymmetricKeyFactory.key_type_map:
            symmetric_key = SymmetricKeyFactory.key_type_map[key_type]
            return symmetric_key(bits, key)
        msg: str = "Invalid Symmetric key"
        raise TypeError(msg)

    @staticmethod
    def get_key(key_type: str) -> Symmetric:
        if key_type in SymmetricKeyFactory.key_type_map:
            return SymmetricKeyFactory.key_type_map[key_type]
        msg: str = "Invalid Symmetric key"
        raise TypeError(msg)


if __name__ == "__main__":
    SymmetricKeyFactory.create_key(None, None, None)

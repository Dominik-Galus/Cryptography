from src.keys.factories.keyfactory import KeyFactory
from src.keys.symmetric.aes import AES
from src.keys.symmetric.symmetric import Symmetric


class SymmetricKeyFactory(KeyFactory):

    key_type_map: dict[str, Symmetric] = {"AES": AES}

    @staticmethod
    def create_key(key_type: str, bits: int, key=None) -> Symmetric:
        if key_type in SymmetricKeyFactory.key_type_map:
            symmetric_key = SymmetricKeyFactory.key_type_map[key_type]
            return symmetric_key(bits, key)
        raise TypeError("Invalid Symmetric key")

    @staticmethod
    def get_key(key_type: str) -> Symmetric:
        if key_type in SymmetricKeyFactory.key_type_map:
            return SymmetricKeyFactory.key_type_map[key_type]
        raise TypeError("Invalid Symmetric key")


if __name__ == "__main__":
    SymmetricKeyFactory.create_key(None, None, None)

from src.keys.symmetric.symmetric import Symmetric
from src.keys.factories.symmetrickeyfactory import SymmetricKeyFactory


class Session:
    def __init__(self, symmetric_type: Symmetric, symmetric_key, bits: int, server_id: int) -> None:
        self.symmetric_key: Symmetric = symmetric_key
        self.bits = bits
        self.symmetric_type = symmetric_type
        self.id: int = server_id

    def encrypt_data(self, data: str) -> str:
        symmetric_key = SymmetricKeyFactory.create_key(self.symmetric_type, self.bits, self.symmetric_key)
        return symmetric_key.encrypt(data)

    def decrypt_data(self, data):
        symmetric_key = SymmetricKeyFactory.create_key(self.symmetric_type, self.bits, self.symmetric_key)
        return symmetric_key.decrypt(data)

if __name__ == "__main__":
    Session(None, None, None, None)
from src.keys.factories.symmetrickeyfactory import SymmetricKeyFactory
from src.keys.symmetric.symmetric import Symmetric


class Session:
    def __init__(
        self,
        symmetric_type: Symmetric,
        symmetric_key: list[str],
        bits: int,
        server_id: int,
    ) -> None:
        self.symmetric_key: Symmetric = symmetric_key
        self.bits = bits
        self.symmetric_type = symmetric_type
        self.id: int = server_id

    def encrypt_data(self, data: str) -> str:
        symmetric_key: Symmetric = SymmetricKeyFactory.create_key(
            self.symmetric_type, self.bits, self.symmetric_key
        )
        return symmetric_key.encrypt(data)

    def decrypt_data(self, data):
        symmetric_key: Symmetric = SymmetricKeyFactory.create_key(
            self.symmetric_type, self.bits, self.symmetric_key
        )
        return symmetric_key.decrypt(data)


if __name__ == "__main__":
    Session(None, None, None, None)

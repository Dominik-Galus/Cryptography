import numpy as np
from aes import AES


class Session:
    def __init__(self, aes_key: np.ndarray, server_id: int) -> None:
        self.aes_key: np.ndarray = aes_key
        self.id: int = server_id

    def encrypt_data(self, data: str) -> str:
        aes = AES(128, aes_key=self.aes_key)
        return aes.encrypt(data)

    def decrypt_data(self, data):
        aes = AES(128, aes_key=self.aes_key)
        return aes.decrypt(data)

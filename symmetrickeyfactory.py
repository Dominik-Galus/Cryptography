from keyfactory import KeyFactory
from symmetric import Symmetric
from aes import AES


class SymmetricKeyFactory(KeyFactory):
    
    @staticmethod
    def create_key(key_type: str, bits: int) -> Symmetric:
        if key_type.lower() == "aes":
            return AES(bits)
        raise TypeError("Invalid Symmetric key")
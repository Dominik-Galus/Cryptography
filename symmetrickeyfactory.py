from keyfactory import KeyFactory
from symmetric import Symmetric
from aes import AES


class SymmetricKeyFactory(KeyFactory):
    
    key_type_map: dict[str, Symmetric] = {
        "AES": AES
    }
    
    @staticmethod
    def create_key(key_type: str, bits: int, key = None) -> Symmetric:
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
    aes1 = SymmetricKeyFactory.create_key("AES", 128, None)
    aes2 = SymmetricKeyFactory.create_key("AES", 128, aes1.key)
    encrypted_message = aes1.encrypt("Secret message")
    decrypted_message = aes2.decrypt(encrypted_message)
    assert decrypted_message == "Secret message"
    
from asymmetric import Asymmetric
from keyfactory import KeyFactory
from rsa import RSA


class AsymmetricKeyFactory(KeyFactory):
    
    key_type_map: dict[str, Asymmetric] = {
        "RSA": RSA,
    }
    
    @staticmethod
    def create_key(key_type: str, bits: int) -> Asymmetric:
        if key_type in AsymmetricKeyFactory.key_type_map:
            asymmetric_key = AsymmetricKeyFactory.key_type_map[key_type]
            return asymmetric_key(bits)
        raise TypeError("Invalid Asymmetric Key")
    
    @staticmethod
    def get_key(key_type: str):
        if key_type in AsymmetricKeyFactory.key_type_map:
            return AsymmetricKeyFactory.key_type_map[key_type]
        raise TypeError("Invallid Asymmetric Key")
    
if __name__ == "__main__":
    rsa1 = AsymmetricKeyFactory.create_key("RSA", 1024)
    encrypted_message = rsa1.encrypt("1234567")
    decrypted_message = rsa1.decrypt(list(encrypted_message))
    assert decrypted_message == "1234567"
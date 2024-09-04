from keyfactory import KeyFactory
from asymmetric import Asymmetric
from rsa import RSA

class AsymmetricKeyFactory(KeyFactory):
    
    key_type_map: dict[str, Asymmetric] = {
        "RSA": RSA,
    }
    
    @staticmethod
    def create_key(key_type: str, bits: int) -> Asymmetric:
        key_class = AsymmetricKeyFactory.key_type_map[key_type]
        return key_class(bits)
    
    @staticmethod
    def get_key(key_type: str):
        return AsymmetricKeyFactory.key_type_map[key_type]
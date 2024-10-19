from cryptography.src.keys.asymmetric.asymmetric import Asymmetric
from cryptography.src.keys.asymmetric.rsa import RSA
from cryptography.src.keys.factories.keyfactory import KeyFactory


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
    AsymmetricKeyFactory.create_key(None, None)

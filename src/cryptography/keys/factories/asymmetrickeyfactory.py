from typing import ClassVar

from cryptography.keys.asymmetric.asymmetric import Asymmetric
from cryptography.keys.asymmetric.rsa import RSA
from cryptography.keys.factories.keyfactory import KeyFactory


class AsymmetricKeyFactory(KeyFactory):

    key_type_map: ClassVar[dict[str, type[Asymmetric]]] = {
        "RSA": RSA,
    }

    @staticmethod
    def create_key(key_type: str, bits: int) -> Asymmetric:
        if key_type in AsymmetricKeyFactory.key_type_map:
            asymmetric_key = AsymmetricKeyFactory.key_type_map[key_type]
            return asymmetric_key(bits)
        msg: int = "Invalid Asymmetric Key"
        raise TypeError(msg)

    @staticmethod
    def get_key(key_type: str) -> type[Asymmetric]:
        if key_type in AsymmetricKeyFactory.key_type_map:
            return AsymmetricKeyFactory.key_type_map[key_type]
        msg: str = "Invallid Asymmetric Key"
        raise TypeError(msg)


if __name__ == "__main__":
    AsymmetricKeyFactory.create_key(None, None)

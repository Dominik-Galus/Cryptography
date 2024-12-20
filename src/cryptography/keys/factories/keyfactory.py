from abc import ABC, abstractmethod

from cryptography.keys.asymmetric.asymmetric import Asymmetric
from cryptography.keys.symmetric.symmetric import Symmetric


class KeyFactory(ABC):

    @staticmethod
    @abstractmethod
    def create_key(key_type: str, bits: int) -> Symmetric | Asymmetric:
        pass

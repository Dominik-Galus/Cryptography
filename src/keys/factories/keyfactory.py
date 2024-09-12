from abc import ABC, abstractmethod

from src.keys.asymmetric.asymmetric import Asymmetric
from src.keys.symmetric.symmetric import Symmetric


class KeyFactory(ABC):

    @staticmethod
    @abstractmethod
    def create_key(self, key_type, bits) -> Symmetric | Asymmetric:
        pass

import numpy as np

from abc import ABC, abstractmethod


class Symmetric(ABC):

    @abstractmethod
    def encrypt(self, message: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, message: str) -> str:
        pass

    @property
    @abstractmethod
    def key(self) -> np.ndarray:
        pass

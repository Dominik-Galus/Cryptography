from abc import ABC, abstractmethod

import numpy as np


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

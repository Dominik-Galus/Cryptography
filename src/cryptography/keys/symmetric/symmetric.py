from abc import ABC, abstractmethod

import numpy as np
from pydantic import BaseModel


class Symmetric(ABC, BaseModel):

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

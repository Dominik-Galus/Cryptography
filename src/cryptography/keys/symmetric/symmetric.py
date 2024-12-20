from abc import ABC, abstractmethod

import numpy as np
from pydantic import BaseModel, ConfigDict


class Symmetric(ABC, BaseModel):
    key: np.ndarray
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @abstractmethod
    def encrypt(self, message: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, message: str) -> str:
        pass

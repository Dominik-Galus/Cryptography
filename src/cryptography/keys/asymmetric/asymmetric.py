from abc import ABC, abstractmethod

from pydantic import BaseModel, ConfigDict


class Asymmetric(ABC, BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    private_key: tuple[int, int] | int
    public_key: tuple[int, int] | int

    @abstractmethod
    def encrypt(self, message: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, encrypted_message: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def encrypt_with_known_key(message: str, public_key: tuple[int, int]) -> str:
        pass

    @staticmethod
    @abstractmethod
    def decrypt_with_known_key(
        encrypted_message: str, private_key: tuple[int, int],
    ) -> str:
        pass

    @staticmethod
    @abstractmethod
    def load_from_file(content: str) -> tuple[int, int]:
        pass

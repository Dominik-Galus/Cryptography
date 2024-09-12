from abc import ABC, abstractmethod


class Asymmetric(ABC):

    @abstractmethod
    def encrypt(self, message: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, encrypted_message: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def encrypt_with_known_key(self, message: str, public_key: tuple[int, int]) -> str:
        pass

    @staticmethod
    @abstractmethod
    def decrypt_with_known_key(self, encrypted_message: str, private_key: tuple[int, int]) -> str:
        pass

    @property
    @abstractmethod
    def private_key(self) -> tuple[int, int]:
        pass

    @property
    @abstractmethod
    def public_key(self) -> tuple[int, int]:
        pass

    @staticmethod
    @abstractmethod
    def load_from_file(self, content: str) -> tuple[int, int]:
        pass

from abc import ABC, abstractmethod


class IKey(ABC):
    
    @abstractmethod
    def encrypt(self, plain_text):
        pass
    
    @abstractmethod
    def decrypt(self, cipher_text):
        pass
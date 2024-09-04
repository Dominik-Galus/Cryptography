from abc import ABC, abstractmethod

class Symmetric(ABC):
    
    @abstractmethod
    def encrypt(self, message):
        pass
    
    @abstractmethod
    def decrypt(self, message):
        pass
    
    @property
    @abstractmethod
    def key(self):
        pass
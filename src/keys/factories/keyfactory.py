from abc import ABC, abstractmethod


class KeyFactory(ABC):
    
    @staticmethod
    @abstractmethod
    def create_key(self, key_type, bits):
        pass
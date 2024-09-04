from abc import ABC, abstractmethod


class Asymmetric(ABC):
    
    @abstractmethod
    def encrypt(self, message):
        pass
    
    @abstractmethod
    def decrypt(self, encrypted_message):
        pass
    
    @staticmethod
    @abstractmethod
    def encrypt_with_known_key(self, message, public_key):
        pass
    
    @staticmethod
    @abstractmethod
    def decrypt_with_known_key(self, encrypted_message, private_key):
        pass
    
    @property
    @abstractmethod
    def private_key(self):
        pass
    
    @property
    @abstractmethod
    def public_key(self):
        pass
    
    @staticmethod
    @abstractmethod
    def load_from_file(self, content):
        pass
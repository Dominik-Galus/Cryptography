from abc import ABC, abstractmethod

class Restriction(ABC):
    
    @abstractmethod
    def check(self, value: int) -> int:
        pass
    
    @abstractmethod
    def add(self, value1: int, value2: int) -> int:
        pass
    
    @abstractmethod
    def mul(self, value1: int, value2: int) -> int:
        pass
    
    @abstractmethod
    def modulo(self) -> int:
        pass
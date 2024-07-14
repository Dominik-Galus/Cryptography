from pure import *
from math import gcd, lcm
from random import randrange
from number import Number
from restrictions.ring import Ring

class RSA:
    
    def __init__(self, bits: int) -> None:
        self.n = self.generate_n(bits)
        self.public_key, self.private_key = self.generate_keys()
    
    def encrypt(self, plain_text: str) -> list[int]:
        num_obj, _ = self.public_key
        cipher = [pow(ord(char), num_obj.value, self.n) for char in plain_text]
        return cipher
    
    def decrypt(self, cipher_text: str) -> int:
        num_obj, _ = self.private_key
        temp = [str(pow(int(char), num_obj.value, self.n)) for char in cipher_text]
        plain = [chr(int(char)) for char in temp]
        return "".join(plain)
    
    def generate_keys(self) -> tuple[tuple[Number, int]]:
        
        self.phi: int = lcm(self.p-1, self.q-1)
        self.ring = Ring(self.phi)
        
        temp: int = randrange(1, self.phi)
        e = Number(temp, self.ring)
        g = gcd(e.value, self.phi)
        while g != 1:
            e.value = randrange(1, self.phi)
            g = gcd(e.value, self.phi)
        
        temp = self.ring.mult_inverse(e.value)
        d = Number(temp, self.ring)
        
        return ((e, self.n), (d, self.n))
    
    def generate_n(self, bits: int) -> int:
        self.p: int = self.generate_large_prime(int(bits/2))
        self.q: int = self.generate_large_prime(int(bits/2))
        return self.p * self.q
        
    def generate_large_prime(self, bits: int) -> int:
        p = randrange((2**(bits-1))+1, (2**bits)-1)
        while not is_prime(p):
            p = randrange((2**(bits-1))+1, (2**bits)-1)
        return p
        

if __name__ == "__main__":
    r = RSA(2048)
    s1: str = r.encrypt("Hello")
    assert r.decrypt(s1) == "Hello"
    s2: str = r.encrypt("Welcome to my kitchen")
    assert r.decrypt(s2) == "Welcome to my kitchen"
    
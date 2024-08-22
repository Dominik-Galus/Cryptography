from math import lcm
from random import randrange
import numpy as np

from number import Number
from pure import is_prime
from restrictions.ring import Ring


class RSA:

    def __init__(self, bits: int) -> None:
        self.n = self.generate_n(bits)
        self.public_key, self.private_key = self.generate_keys()

    def encrypt(self, plain_text: str) -> int:
        e, n = self.public_key
        cipher = pow(int(plain_text), e, n)
        return cipher

    def decrypt(self, cipher_text: list[int]) -> list[int]:
        d, n = self.private_key
        decrypted_numbers = [pow(char, d, n) for char in cipher_text]
        return decrypted_numbers
    
    @staticmethod
    def encrypt_with_known_key(plain_text: str, public_key: tuple[int, int]) -> int:
        cipher: int = pow(int(plain_text), public_key[0], public_key[1])
        return cipher
    
    @staticmethod
    def decrypt_with_known_key(cipher_text: list[int], private_key: tuple[int, int]) -> list[int]:
        decrypted_numbers: list[int] = [pow(char, private_key[0], private_key[1]) for char in cipher_text]
        return decrypted_numbers

    def generate_keys(self) -> tuple[tuple[int, int]]:

        self.phi: int = lcm(self.p - 1, self.q - 1)
        self.ring = Ring(self.phi)

        candidate: int = randrange(1, self.phi)
        e = Number(candidate, self.ring)
        g = e.gcd(self.phi)
        while g != 1:
            candidate = randrange(1, self.phi)
            e = Number(candidate, self.ring)
            g = e.gcd(self.phi)

        temp = self.ring.mult_inverse(e.value)
        d = Number(temp, self.ring)

        return ((e.value, self.n), (d.value, self.n))

    def generate_n(self, bits: int) -> int:
        self.p: int = self.generate_large_prime(int(bits / 2))
        self.q: int = self.generate_large_prime(int(bits / 2))
        return self.p * self.q

    def generate_large_prime(self, bits: int) -> int:
        p = randrange((2 ** (bits - 1)) + 1, (2**bits) - 1)
        while not is_prime(p):
            p = randrange((2 ** (bits - 1)) + 1, (2**bits) - 1)
        return p


if __name__ == "__main__":
    r = RSA(1024)
    print(r.phi)
    print("******************")
    print(r.public_key[0])
    print("***************************")
    print(r.public_key[1])
    print("***************************************************************")
    print(r.private_key[0])
    print("**********************")
    print(r.private_key[1])
    xd = np.array([[ 60,  16, 201, 179],
                    [ 53, 107, 179,  22],
                    [ 60,  70, 202,  47],
                    [139,  10, 244,  15]])
    encrypted_aes_key = [
            r.encrypt(str(byte)) for byte in xd.flatten()
        ]
    
    decrypted_integers = r.decrypt(encrypted_aes_key)  # List of decrypted integers
    aes_key = np.array(decrypted_integers, dtype=np.uint8).reshape(4,4)
    
    assert xd.all() == aes_key.all()
    
    encrypted_aes_key = [
        RSA.encrypt_with_known_key(str(byte), r.public_key) for byte in xd.flatten()
    ]
    
    decrypted_integers = RSA.decrypt_with_known_key(encrypted_aes_key, r.private_key)
    aes_key = np.array(decrypted_integers, dtype=np.uint8).reshape(4,4)
    
    assert xd.all() == aes_key.all()

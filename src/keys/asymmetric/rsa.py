from math import lcm
from random import randrange

import numpy as np

from src.keys.asymmetric.asymmetric import Asymmetric
from src.algebra.number import Number
from src.algebra.pure import is_prime
from src.algebra.restrictions.ring import Ring


class RSA(Asymmetric):

    def __init__(self, bits: int) -> None:
        self.n = self.generate_n(bits)
        self._public_key, self._private_key = self.generate_keys()

    def encrypt(self, message: str) -> str:
        e, n = self.public_key
        cipher = [pow(ord(char), e, n) for char in message]
        encrypted_message = ''.join([str(num).zfill(len(str(n))) for num in cipher])
        return encrypted_message

    def decrypt(self, encrypted_message: str) -> str:
        d, n = self.private_key
        block_size = len(str(n))
        encrypted_numbers = [int(encrypted_message[i:i+block_size]) for i in range(0, len(encrypted_message), block_size)]
        decrypted_chars = [chr(pow(num, d, n)) for num in encrypted_numbers]
        return ''.join(decrypted_chars)

    @staticmethod
    def encrypt_with_known_key(message: str, public_key: tuple[int, int]) -> str:
        
        cipher: list[int] = [pow(ord(char), public_key[0], public_key[1]) for char in message]
        encrypted_message: str = ''.join([str(num).zfill(len(str(public_key[1]))) for num in cipher])
        
        return encrypted_message

    @staticmethod
    def decrypt_with_known_key(encrypted_message: str, private_key: tuple[int, int]) -> str:
        block_size: int = len(str(private_key[1]))
        encrypted_numbers = [int(encrypted_message[i:i+block_size]) for i in range(0, len(encrypted_message), block_size)]
        decrypted_chars = [chr(pow(num, private_key[0], private_key[1])) for num in encrypted_numbers]
        return ''.join(decrypted_chars)

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
    
    @property
    def private_key(self):
        return self._private_key
    
    @property
    def public_key(self):
        return self._public_key
    
    @staticmethod
    def load_from_file(content: str) -> tuple[int, int]:
        keys: list[str] = content.split()
        return (int(keys[0]), int(keys[1]))


if __name__ == "__main__":
    r = RSA(2048)
    message = "Secret message"
    encrypted = r.encrypt(message)
    decrypted = r.decrypt(encrypted)
    decr = RSA.decrypt_with_known_key(encrypted, r._private_key)
    assert decrypted == message and decr == message
    print(encrypted)
    print(decrypted)
    print(decr)
    
    # xd = np.array(
    #     [[60, 16, 201, 179], [53, 107, 179, 22], [60, 70, 202, 47], [139, 10, 244, 15]]
    # )
    # print(xd.shape)
    # encrypted_aes_key = [r.encrypt(str(byte)) for byte in xd.flatten()]
    # print(encrypted_aes_key)

    # decrypted_integers = [r.decrypt(char) for char in encrypted_aes_key]
    # print(decrypted_integers)
    # # decrypted_integers = r.decrypt(encrypted_aes_key)  # List of decrypted integers
    # # print(decrypted_integers)
    # aes_key = np.array(decrypted_integers, dtype=np.uint8).reshape(4, 4)

    # assert xd.all() == aes_key.all()

    # encrypted_aes_key = [
    #     RSA.encrypt_with_known_key(str(byte), r.public_key) for byte in xd.flatten()
    # ]

    # decrypted_integers = RSA.decrypt_with_known_key(encrypted_aes_key, r.private_key)
    # aes_key = np.array(decrypted_integers, dtype=np.uint8).reshape(4, 4)

    # assert xd.all() == aes_key.all()

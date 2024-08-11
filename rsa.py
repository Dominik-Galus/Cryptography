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
        num_obj, n = self.public_key
        cipher = pow(int(plain_text), num_obj.value, n)
        return cipher

    def decrypt(self, cipher_text: list[int]) -> int:
        num_obj, n = self.private_key
        decrypted_numbers = [pow(char, num_obj.value, n) for char in cipher_text]
        return decrypted_numbers

    def generate_keys(self) -> tuple[tuple[Number, int]]:

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

        return ((e, self.n), (d, self.n))

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
    print(r.private_key)
    print(r.public_key)
    xd = np.array([[ 60,  16, 201, 179],
                    [ 53, 107, 179,  22],
                    [ 60,  70, 202,  47],
                    [139,  10, 244,  15]])
    print(xd)
    print(xd.size)
    print("***********************************************************************")
    encrypted_aes_key = [
            r.encrypt(str(byte)) for byte in xd.flatten()
        ]
    print(encrypted_aes_key)
    print(len(encrypted_aes_key))
    print("***********************************************************************")
    
    decrypted_integers = r.decrypt(encrypted_aes_key)  # List of decrypted integers
    aes_key = np.array(decrypted_integers, dtype=np.uint8).reshape(4,4)
    print(decrypted_integers)
    print(aes_key)
    # decrypted_bytes = []
    # for decrypted_int in decrypted_integers:
    #     decrypted_byte = decrypted_int & 0xFF  # Extract the least significant byte
    #     decrypted_bytes.append(decrypted_byte)

    # aes_key = np.array(decrypted_bytes, dtype=np.uint8).reshape(4, 4)
    # print(aes_key)
    # print(aes_key.size)

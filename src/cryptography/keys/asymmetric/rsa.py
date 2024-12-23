from math import lcm
from random import randrange

from pydantic import Field

from cryptography.algebra.number import Number
from cryptography.algebra.pure import is_prime
from cryptography.algebra.restrictions.ring import Ring
from cryptography.keys.asymmetric.asymmetric import Asymmetric


class RSA(Asymmetric):
    n: int = Field(default=0)
    p: int = Field(default=0)
    q: int = Field(default=0)

    def __init__(self, bits: int) -> None:
        super().__init__(private_key=(0, 0), public_key=(0, 0))
        self.n = self.generate_n(bits)
        self.public_key, self.private_key = self.generate_keys()

    def encrypt(self, message: str) -> str:
        e, n = self.public_key
        cipher = [pow(ord(char), e, n) for char in message]
        return "".join([str(num).zfill(len(str(n))) for num in cipher])

    def decrypt(self, encrypted_message: str) -> str:
        d, n = self.private_key
        block_size = len(str(n))
        encrypted_numbers = [
            int(encrypted_message[i : i + block_size])
            for i in range(0, len(encrypted_message), block_size)
        ]
        decrypted_chars = [chr(pow(num, d, n)) for num in encrypted_numbers]
        return "".join(decrypted_chars)

    @staticmethod
    def encrypt_with_known_key(message: str, public_key: tuple[int, int]) -> str:

        cipher: list[int] = [
            pow(ord(char), public_key[0], public_key[1]) for char in message
        ]
        encrypted_message: str = "".join(
            [str(num).zfill(len(str(public_key[1]))) for num in cipher],
        )

        return encrypted_message

    @staticmethod
    def decrypt_with_known_key(
        encrypted_message: str, private_key: tuple[int, int],
    ) -> str:
        block_size: int = len(str(private_key[1]))
        encrypted_numbers = [
            int(encrypted_message[i : i + block_size])
            for i in range(0, len(encrypted_message), block_size)
        ]
        decrypted_chars = [
            chr(pow(num, private_key[0], private_key[1])) for num in encrypted_numbers
        ]
        return "".join(decrypted_chars)

    def generate_keys(self) -> tuple[tuple[int, int]]:

        phi: int = lcm(self.p - 1, self.q - 1)
        ring = Ring(phi)

        candidate: int = randrange(1, phi)
        e = Number(candidate, ring)
        g = e.gcd(phi)
        while g != 1:
            candidate = randrange(1, phi)
            e = Number(candidate, ring)
            g = e.gcd(phi)

        temp = ring.mult_inverse(e.value)
        d = Number(temp, ring)

        return ((e.value, self.n), (d.value, self.n))

    def generate_n(self, bits: int) -> int:
        self.p: int = self.generate_large_prime(int(bits / 2))
        self.q: int = self.generate_large_prime(int(bits / 2))
        return self.p * self.q

    def generate_large_prime(self, bits: int) -> int:
        p: int = randrange((2 ** (bits - 1)) + 1, (2**bits) - 1)
        while not is_prime(p):
            p: int = randrange((2 ** (bits - 1)) + 1, (2**bits) - 1)
        return p

    @staticmethod
    def load_from_file(content: str) -> tuple[int, int]:
        limit_key_size: int = 2
        keys: list[str] = content.split()
        if len(keys) != limit_key_size:
            msg: str = "Too much content in file"
            raise IndexError(msg)
        return (int(keys[0]), int(keys[1]))


if __name__ == "__main__":
    RSA(None)

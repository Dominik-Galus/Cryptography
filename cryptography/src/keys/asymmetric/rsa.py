from math import lcm
from random import randrange

from cryptography.src.algebra.number import Number
from cryptography.src.algebra.pure import is_prime
from cryptography.src.algebra.restrictions.ring import Ring
from cryptography.src.keys.asymmetric.asymmetric import Asymmetric


class RSA(Asymmetric):

    def __init__(self, bits: int) -> None:
        self.n = self.generate_n(bits)
        self._public_key, self._private_key = self.generate_keys()

    def encrypt(self, message: str) -> str:
        e, n = self.public_key
        cipher = [pow(ord(char), e, n) for char in message]
        encrypted_message = "".join([str(num).zfill(len(str(n))) for num in cipher])
        return encrypted_message

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
            [str(num).zfill(len(str(public_key[1]))) for num in cipher]
        )

        return encrypted_message

    @staticmethod
    def decrypt_with_known_key(
        encrypted_message: str, private_key: tuple[int, int]
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
        p: int = randrange((2 ** (bits - 1)) + 1, (2**bits) - 1)
        while not is_prime(p):
            p: int = randrange((2 ** (bits - 1)) + 1, (2**bits) - 1)
        return p

    @property
    def private_key(self) -> tuple[int, int]:
        return self._private_key

    @property
    def public_key(self) -> tuple[int, int]:
        return self._public_key

    @staticmethod
    def load_from_file(content: str) -> tuple[int, int]:
        keys: list[str] = content.split()
        if len(keys) != 2:
            raise Exception("Too much content in file")
        return (int(keys[0]), int(keys[1]))


if __name__ == "__main__":
    RSA(None)

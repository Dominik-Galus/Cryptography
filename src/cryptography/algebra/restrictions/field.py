from cryptography.algebra.pure import is_prime
from cryptography.algebra.restrictions.ring import Ring


class Field(Ring):

    def __init__(self, mod: int) -> None:
        super().__init__(mod)
        if not is_prime(self.mod):
            msg: str = "To create a field parse a prime argument"
            raise TypeError(msg)

    def division(self, a: int, b: int) -> int:
        if a is None or b is None:
            return ValueError("Values can't be None")
        b_inverse: int = self.mult_inverse(b)
        return self.mul(a, b_inverse)


if __name__ == "__main__":
    Field(None)

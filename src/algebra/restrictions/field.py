from src.algebra.pure import is_prime
from src.algebra.restrictions.ring import Ring


class Field(Ring):

    def __init__(self, mod: int) -> None:
        super().__init__(mod)
        if not is_prime(self.mod):
            raise TypeError("To create a field parse a prime argument")

    def division(self, a: int, b: int) -> int:
        b_inverse: int = self.mult_inverse(b)
        return self.mul(a, b_inverse)


if __name__ == "__main__":
    Field(None)

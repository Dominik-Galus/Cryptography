from pure import is_prime
from restrictions.ring import Ring


class Field(Ring):

    def __init__(self, mod: int) -> None:
        super().__init__(mod)
        if is_prime(self.mod, 1000) == False:
            raise TypeError("To create a field parse a prime argument")

    def division(self, a: int, b: int) -> int:
        b_inverse: int = self.mult_inverse(b)
        return self.mul(a, b_inverse)

if __name__ == "__main__":

    Z_7 = Field(7)

    assert Z_7.additive_inverse(2) == 5
    assert Z_7.mult_inverse(3) == 5
    assert Z_7.division(3, 4) == 6

from restrictions.ring import Ring
from pure import is_prime


class Field(Ring):

    def __init__(self, mod: int) -> None:
        super().__init__(mod)
        if is_prime(self.mod) == False:
            raise TypeError("To create a field parse a prime argument")

    def division(self, a: int, b: int) -> int:
        b_inverse: int = self.mult_inverse(b)
        return self.mul(a, b_inverse)


Z_7 = Field(7)

assert Z_7.additive_inverse(2) == 5
assert Z_7.mult_inverse(3) == 5
assert Z_7.division(3, 4) == 6

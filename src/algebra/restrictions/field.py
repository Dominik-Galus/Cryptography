from src.algebra.pure import is_prime
from src.algebra.restrictions.ring import Ring


class Field(Ring):

    def __init__(self, mod: int) -> None:
        super().__init__(mod)
        if is_prime(self.mod) == False:
            raise TypeError("To create a field parse a prime argument")

    def division(self, a: int, b: int) -> int:
        b_inverse: int = self.mult_inverse(b)
        return self.mul(a, b_inverse)

if __name__ == "__main__":

    r1 = Field(59)
    r2 = Field(787)
    r3 = Field(13)
    r4 = Field(12391)
    r5 = Field(239489)
    r6 = Field(1009)
    print(r1.division(35, 99))
    print(r2.division(1000, 543))
    print(r3.division(92, 965))
    print(r4.division(387472, 6955486))
    print(r5.division(758494, 923444))
    print(r6.division(9765, 12385534))

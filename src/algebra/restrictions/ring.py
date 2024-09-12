from math import gcd

from src.algebra.restrictions.group import Group


class Ring(Group):

    def __init__(self, mod: int) -> None:
        super().__init__(mod)
        self.i = 1

    def mult_inverse(self, value: int) -> int:
        if value % self.mod == 0:
            raise ValueError("Can't find the multiplicative inversion for 0")
        if gcd(self.mod, value) != 1:
            return None
        temp_mod: int = self.mod
        q: int = int(temp_mod / value)
        r: int = temp_mod % value
        t1: int = 0
        t2: int = 1
        t3: int = t1 - (q * t2)
        while r != 0:
            temp_mod = value
            value = r
            q = int(temp_mod / value)
            r = temp_mod % value
            t1 = t2
            t2 = t3
            t3 = t1 - (q * t2)
        t2 = t2 % self.mod
        if t2 < 0:
            t2 += self.mod
        return t2

    def mul(self, value1: int, value2: int) -> int:
        if value1 % self.mod == 0 or value2  % self.mod == 0:
            raise ValueError("Can't multiply with 0")
        result: int = (value1 * value2) % self.mod
        result = result + self.mod if result < 0 else result
        return result


if __name__ == "__main__":
    r1 = Ring(55)
    r2 = Ring(780)
    r3 = Ring(13)
    r4 = Ring(12394)
    r5 = Ring(239483)
    r6 = Ring(1000)
    print(r1.mult_inverse(35))
    print(r2.mult_inverse(1000))
    print(r3.mult_inverse(965))
    print(r4.mult_inverse(387472))
    print(r5.mult_inverse(758494))
    print(r6.mult_inverse(9765))

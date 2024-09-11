from math import gcd

from src.algebra.restrictions.group import Group


class Ring(Group):

    def __init__(self, mod: int) -> None:
        super().__init__(mod)
        self.i = 1

    def mult_inverse(self, value: int) -> int:
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
        result: int = (value1 * value2) % self.mod
        result = result + self.mod if result < 0 else result
        return result


if __name__ == "__main__":
    r = Ring(5)
    assert r.add(3, 4) == 2
    assert r.check(13) == 3
    assert r.mul(2, 4) == 3
    assert r.additive_inverse(3) == 2
    assert r.mult_inverse(2) == 3
    r2 = Ring(780)
    assert r2.mult_inverse(17) == 413
    r3 = Ring(26)
    assert r3.mult_inverse(11) == 19

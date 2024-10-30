from math import gcd

from cryptography.src.algebra.restrictions.group import Group


class Ring(Group):

    def __init__(self, mod: int) -> None:
        super().__init__(mod)
        self.i = 1

    def mult_inverse(self, value: int) -> int | None:
        if value is None:
            raise ValueError("Value can't be None")
        if value % self.mod == 0:
            return None
        if gcd(self.mod, value) != 1:
            return None
        mod_base: int = self.mod
        quotient: int = mod_base // value
        remainder: int = mod_base % value
        prev_coef: int = 0
        curr_coef: int = 1
        next_coef: int = prev_coef - (quotient * curr_coef)

        while remainder != 0:
            mod_base = value
            value = remainder
            quotient = mod_base // value
            remainder = mod_base % value
            prev_coef, curr_coef = curr_coef, next_coef
            next_coef = prev_coef - (quotient * curr_coef)

        curr_coef = curr_coef % self.mod
        if curr_coef < 0:
            curr_coef += self.mod
        return curr_coef

    def mul(self, value1: int, value2: int) -> int |  None:
        if value1 % self.mod == 0 or value2 % self.mod == 0:
            return None
        result: int = (value1 * value2) % self.mod
        result = result + self.mod if result < 0 else result
        return result


if __name__ == "__main__":
    Ring(None)

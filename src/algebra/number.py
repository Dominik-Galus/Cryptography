from math import gcd
from typing import Self

from src.algebra.restrictions.restriction import Restriction


class Number:
    def __init__(self, value: int, restriction: Restriction) -> None:
        self.restriction = restriction
        self.value = self.restriction.check(value)

    def __add__(self, other: int | Self) -> Self:
        if type(other) is int:
            return Number(self.restriction.add(self.value, other), self.restriction)
        elif (
            type(self.restriction) is type(other.restriction)
            and self.restriction.modulo() == other.restriction.modulo()
        ):
            return Number(
                self.restriction.add(self.value, other.value), self.restriction
            )
        else:
            raise ValueError("Numbers can be added only with the same restriction")

    def __mul__(self, other: int | Self) -> Self:
        if type(other) is int:
            return Number(self.restriction.mul(self.value, other), self.restriction)
        elif (
            type(self.restriction) is type(other.restriction)
            and self.restriction.modulo() == other.restriction.modulo()
        ):
            return Number(
                self.restriction.mul(self.value, other.value), self.restriction
            )
        else:
            raise ValueError("Numbers can be multiplied only with the same restriction")

    def gcd(self, number: int) -> int:
        return gcd(self.value, number)

    __radd__ = __add__
    __rmul__ = __mul__


if __name__ == "__main__":
    Number(None, None)

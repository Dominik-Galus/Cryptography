from cryptography.algebra.restrictions.restriction import Restriction


class Group(Restriction):

    def __init__(self, mod: int) -> None:
        if mod is None:
            msg: str = "Modulo can't be None"
            raise ValueError(msg)
        if mod < 0:
            msg: str = "Modulo must be positive"
            raise ValueError(msg)
        self.mod = mod
        self.e: int = 0

    def additive_inverse(self, value: int) -> int:
        if value is None:
            msg: str = "Value can't be None"
            raise ValueError(msg)
        value = value % self.mod
        if value < 0:
            value += self.mod
        inverse: int = self.mod - value
        return inverse

    def add(self, value1: int, value2: int) -> int:
        if value1 is None or value2 is None:
            msg: str = "Values can't be None"
            raise ValueError(msg)
        result: int = (value1 + value2) % self.mod
        if result < 0:
            result += self.mod
        return result

    def check(self, value: int) -> int | None:
        if value is None:
            msg: str = "Value can't be None"
            raise ValueError(msg)
        if value >= self.mod:
            value = value % self.mod
        elif value < 0:
            value = value % self.mod
            value += self.mod
        return value

    def mul(self, value1: int, value2: int) -> int:
        raise NotImplementedError

    def modulo(self) -> int:
        return self.mod


if __name__ == "__main__":
    Group(None)

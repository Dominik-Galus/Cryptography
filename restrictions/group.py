from restrictions.restriction import Restriction


class Group(Restriction):

    def __init__(self, mod: int) -> None:
        if mod < 0:
            raise ValueError("Modulo must be positive")
        self.mod = mod
        self.e = 0

    def additive_inverse(self, value: int) -> int:
        value = value % self.mod
        if value < 0:
            value += self.mod
        inverse: int = self.mod - value
        return inverse

    def add(self, value1: int, value2: int) -> int:
        result: int = (value1 + value2) % self.mod
        if result < 0:
            result += self.mod
        return result

    def check(self, value: int) -> int:
        if value >= self.mod:
            value = value % self.mod
        elif value < 0:
            value = value % self.mod
            value += self.mod
        return value

    def mul(self, value1: int, value2: int) -> int:
        raise NotImplementedError()

    def modulo(self) -> int:
        return self.mod


if __name__ == "__main__":
    g = Group(7)

    assert g.add(3, 4) == 0
    assert g.check(13) == 6
    assert g.additive_inverse(4) == 3

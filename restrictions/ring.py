from restrictions.group import Group

class Ring(Group):
    
    def __init__(self, mod: int) -> None:
        super().__init__(mod)
        self.i = 1
        
    def mult_inverse(self, value: int) -> int:
        if value < 0:
            value = value % self.mod
            value += self.mod
        for elem in self.group_elements:
            if (value * elem) % self.mod == self.i:
                return elem
        return None
    
    def mul(self, value1: int, value2: int) -> int:
        result: int = (value1 * value2) % self.mod
        if result < 0:
            result += self.mod
        return result
    
r = Ring(5)
assert r.add(3, 4) == 2
assert r.check(13) == 3
assert r.mul(2, 4) == 3
assert r.additive_inverse(3) == 2
assert r.mult_inverse(2) == 3


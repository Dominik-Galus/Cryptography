
class N_Group:
    
    def __init__(self, mod: int) -> None:
        if mod < 0:
            raise ValueError("Modulo must be positive")
        self.mod = mod
        self.group_elements = list(range(mod))
        self.e = 0
        
    def additive_inverse(self, value: int) -> int:
        if value < 0:
            value = value % self.mod
            value += self.mod
        for elem in self.group_elements:
            if((value + elem) % self.mod == self.e):
                return elem
        return None
            
    def add(self, values: list[int]) -> int:
        result: int = values[0]
        for value in values[1:]:
            result = (result + value) % self.mod
        if result < 0:
            result += self.mod
        return result
    
    
    
C_5 = N_Group(5)

assert C_5.add([10, 17, 21]) == 3
assert C_5.add([-14, -16, -7]) == 3
assert C_5.additive_inverse(-3) == 3
assert C_5.additive_inverse(-16) == 1
assert C_5.add([1,2,3,4,5]) == 0
assert C_5.additive_inverse(3) == 2

class N_Group:
    
    def __init__(self, mod: int) -> None:
        if mod < 0:
            raise ValueError("Modulo must be positive")
        self.mod = mod
        self.group_elements = list(range(mod))
        self.i = 0
        
    def inverse(self, elem: int) -> int:
        if elem < 0:
            elem = elem % self.mod
            elem += self.mod
        for i in self.group_elements:
            if((elem + i) % self.mod == 0):
                return i
            
    def op(self, *args: int) -> int:
        result: int = 0
        for arg in args:
            result = (result + arg) % self.mod
        if result < 0:
            result += self.mod
        return result
    
    
C_5 = N_Group(5)

C_5.inverse(15)

assert C_5.op(10, 17, 21) == 3
assert C_5.op(-14, -16, - 7) == 3
assert C_5.inverse(-3) == 3
assert C_5.inverse(-16) == 1
assert C_5.op(1,2,3,4,5) == 0
assert C_5.inverse(3) == 2
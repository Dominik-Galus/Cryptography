from group import N_Group

class N_Ring(N_Group):
    
    def __init__(self, mod: int) -> None:
        super(N_Ring, self).__init__(mod)
        self.i = 1
        
    def mult_inverse(self, value: int) -> int:
        if value < 0:
            value = value % self.mod
            value += self.mod
        for elem in self.group_elements:
            if (value * elem) % self.mod == self.i:
                return elem
        return None
    
    def multiplication(self, *args: int) -> int:
        result: int = args[0]
        for arg in args[1:]:
            result = (result * arg) % self.mod
        if result < 0:
            result += self.mod
        return result
    
    def operation(self, operations: list[str], values: list[int]) -> int:
        result: int = values[0]
        for i, op in enumerate(operations):
            if op == "add":
                result = self.add(result, values[i+1])
            else:
                result = self.multiplication(result, values[i+1])
        return result
                

Z_5 = N_Ring(5)

assert Z_5.operation(["add", "mult"], [1,5, 4]) == 4
assert Z_5.operation(["add", "mult", "add", "mult"], [4,5,6,7,8]) == 3
assert Z_5.mult_inverse(3) == 2
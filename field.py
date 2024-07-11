from ring import N_Ring
from pure import is_prime

class N_Field(N_Ring):
    
    def __init__(self, mod: int) -> None:
        super(N_Field, self).__init__(mod)
        if is_prime(self.mod) == False:
            raise TypeError("To create a field parse a prime argument")
        
    def division(self, a: int, b: int) -> int:
        b_inverse: int = self.mult_inverse(b)
        return self.multiplication(a, b_inverse)
        
        
Z_7 = N_Field(7)

assert Z_7.additive_inverse(2) == 5
assert Z_7.mult_inverse(3) == 5
assert Z_7.division(3, 4) == 6
assert Z_7.operation(['add', 'add', 'mult', 'add'], [7, 4, 3, 2, 9]) == 2
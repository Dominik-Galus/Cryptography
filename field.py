from ring import N_Ring
from pure import is_prime

class N_Field(N_Ring):
    
    def __init__(self, mod: int) -> None:
        super(N_Field, self).__init__(mod)
        if is_prime(self.mod) == False:
            raise TypeError("To create a field parse an prime argument")
        
    def division(self, a: int, b: int) -> int:
        b_inverse = self.mult_inverse(b)
        return self.multiplication(a, b_inverse)
        
from ring import N_Ring

class Restriction():
    
    def __init__(self, mod: int) -> None:
        self.ring = N_Ring(mod)
        
    def check(self, value: int) -> int:
        if not self.ring.is_element(value):
            value = value % self.ring_modulo()
        if value < 0:
            value += self.ring_modulo
        return value
    
    def add(self, value1: int, value2: int) -> int:
        return self.ring.add([value1, value2])
    
    def mult(self, value1: int, value2: int) -> int:
        return self.ring.multiplication([value1, value2])
    
    def ring_modulo(self) -> int:
        return self.ring.mod
    
r = Restriction(10)
assert r.check(15) == 5
assert r.add(3, 17) == 0
assert r.mult(5, 9) == 5
    
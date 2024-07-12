from restriction import Restriction

class Number:
    def __init__(self, value:int, restriction: Restriction) -> None:
        self.restriction = restriction
        self.restriction.check(value)
        self.value = value
        
    def __add__(self, other: "Number") -> "Number":
        if self.restriction.ring_modulo() != other.restriction.ring_modulo():
            raise ValueError("Numbers can be added with the same restriction")
        return Number(self.restriction.add(
            self.value, other.value
        ), self.restriction)
    
    def __mul__(self, other: "Number") -> "Number":
        if self.restriction.ring_modulo() != other.restriction.ring_modulo():
            raise ValueError("Numbers can be multipilied with the same restriction")
        return Number(self.restriction.mult(
            self.value, other.value
        ), self.restriction)
        
        
n1 = Number(4, Restriction(5))
n2 = Number(3, Restriction(5))
n3 = n1 + n2
n4 = n1 * n2
n5 = (n1 + n3) * n4

assert n3.value == 2
assert n4.value == 2
assert n5.value == 2
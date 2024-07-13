from restrictions.restriction import Restriction
from restrictions.ring import Ring
from typing import Union

class Number:
    def __init__(self, value: int, restriction: Restriction) -> None:
        self.restriction = restriction
        self.value = self.restriction.check(value)
        
    def __add__(self, other: Union[int, "Number"]) -> "Number":
        if type(other) == int:
            return Number(self.restriction.add(self.value, other), self.restriction)
        elif (type(self.restriction) == type(other.restriction) and self.restriction.modulo() == other.restriction.modulo()):
            return Number(
            self.restriction.add(self.value, other.value), self.restriction
            )
        else:
            raise ValueError("Numbers can be added only with the same restriction")
        
    def __mul__(self, other: Union[int, "Number"]) -> "Number":
        if type(other) == int:
            return Number(self.restriction.mul(self.value, other), self.restriction)
        elif (type(self.restriction) == type(other.restriction) and self.restriction.modulo() == other.restriction.modulo()):
            if self.restriction.mul(0,0) == NotImplemented or other.restriction.mul(0,0) == NotImplemented:
                raise ValueError("Can't make multiplication with given restriction")
        return Number(
            self.restriction.mul(self.value, other.value), self.restriction
        )
            
        
n1 = Number(3, Ring(5))
n2 = Number(2, Ring(7))

try:
    n3 = n1+n2
    print(n3.value)
except ValueError as e:
    print(e)
    
n4 = Number(6, Ring(7))
n5 = n2 + n4
assert n5.value == 1
n6 = Number(1, Ring(5))
n7 = n1 + n6
assert n7.value == 4
n8 = n2 * n4
assert n8.value == 5
n9 = (n2 + n4) * n8
assert n9.value == 5

n10 = n1 + 2
assert n10.value == 0
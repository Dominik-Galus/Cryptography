from math import sqrt
from random import randint


def is_prime(value: int, k: int) -> bool:
    if value == 1:
        return False
    elif value == 2 or value == 3:
        return True
    
    else:
        for i in range(k):
            a = randint(2, value - 2)
            if pow(a, value - 1, value) != 1:
                return False
    return True

if __name__ == "__main__":
    k = 100
    assert is_prime(11, k) == True
    assert is_prime(15, k) == False
    assert is_prime(21, k) == False
    assert is_prime(23, k) == True
    assert is_prime(4, k) == False
    assert is_prime(10000023, k) == False
    assert is_prime(234123751237, k) == True
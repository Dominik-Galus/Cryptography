from math import sqrt


def is_prime(value: int) -> bool:
    for i in range(2, int(sqrt(value)) + 1):
        if value % i == 0:
            return False
    return True
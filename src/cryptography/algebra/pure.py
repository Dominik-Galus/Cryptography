from random import randint


def is_prime(value: int, k: int = 1000) -> bool:
    if value == 1:
        return False
    if value in (2, 3):
        return True

    for _ in range(k):
        a = randint(2, value - 2)
        if pow(a, value - 1, value) != 1:
            return False
    return True


if __name__ == "__main__":
    is_prime(None)

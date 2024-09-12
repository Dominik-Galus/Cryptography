from random import getrandbits, randint


def is_prime(value: int, k: int = 1000) -> bool:
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
    assert is_prime(11) == True
    assert is_prime(15) == False
    assert is_prime(21) == False
    assert is_prime(23) == True
    assert is_prime(4) == False
    assert is_prime(10000023) == False
    assert is_prime(234123751237) == True
    assert is_prime(2348723895269) == True
    assert is_prime(2348723895263) == False
    assert is_prime(9548694545637) == False
    assert is_prime(954869454563) == True
    assert is_prime(6546834943597) == False
    assert is_prime(6546834943541) == True
    a = 179769313486231590770839156793787453197860296048756011706444423684197180216158519368947833795864925541502180565485980503646440548199239100050792877003355816639229553136239076508735759914822574862575007425302077447712589550957937778424442426617334727629299387668709205606050270810842907692932019128194467627007
    print(a)
    print(is_prime(a, k=1000))

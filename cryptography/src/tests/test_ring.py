import pytest

from cryptography.src.algebra.restrictions.ring import Ring


class TestRing:

    @pytest.mark.parametrize(
        "test_value1,test_value2,modulo,expected",
        zip(
            [12, 54, 32, 12, 65, 11, 44, 23],
            [65, 88, 43, 33, 1443, 32, 123, -43],
            [11, 54, 64, 34, 76, 55, 12, 77],
            [10, 0, 32, 22, 11, 22, 0, 12],
        ),
    )
    def test_mul(self, test_value1: int, test_value2: int, modulo: int, expected: int) -> None:
        ring = Ring(modulo)
        result: int = ring.mul(test_value1, test_value2)
        assert result == expected

    @pytest.mark.parametrize(
        "test_value, modulo, expected",
        [
            (35, 55, None),
            (1000, 780, None),
            (91, 12, 7),
            (387472, 12394, None),
            (758494, 239483, 23431),
            (9765, 1000, None),
        ],
    )
    def test_mul_inv(self, test_value: int, modulo: int, expected: int) -> None:
        ring = Ring(modulo)
        result: int = ring.mult_inverse(test_value)
        assert result == expected

import pytest

from src.algebra.number import Number
from src.algebra.restrictions.ring import Ring
from src.algebra.restrictions.group import Group


class TestNumber:

    @pytest.mark.parametrize(
        "a,b,c,d",
        zip(
            [12, 54, 32, 12, 65, 11, 44, 23],
            [65, 88, 43, 33, 1443, 32, 123, -43],
            [11, 54, 64, 34, 76, 55, 12, 77],
            [0, 34, 11, 11, 64, 43, 11, 57],
        ),
    )
    def test_add(self, a, b, c, d):
        result1: Number = Number(a, Ring(c)) + Number(b, Ring(c))
        result2: Number = Number(a, Group(c)) + Number(b, Group(c))
        expected: Number = Number(d, Ring(c))
        assert result1.value == expected.value
        assert result2.value == expected.value

        result1 = Number(b, Ring(c)) + Number(a, Ring(c))
        result2 = Number(b, Group(c)) + Number(a, Group(c))
        assert result1.value == expected.value
        assert result2.value == expected.value

    @pytest.mark.parametrize(
        "a,b,c,d",
        zip(
            [12, 54, 32, 12, 65, 11, 44, 23],
            [65, 88, 43, 33, 1443, 32, 123, -43],
            [11, 54, 64, 34, 76, 55, 12, 77],
            [10, 0, 32, 22, 11, 22, 0, 12],
        ),
    )
    def test_mul(self, a, b, c, d):
        result: Number = Number(a, Ring(c)) * Number(b, Ring(c))
        expected: Number = Number(d, Ring(c))
        assert result.value == expected.value

        result = Number(b, Ring(c)) * Number(a, Ring(c))
        assert result.value == expected.value

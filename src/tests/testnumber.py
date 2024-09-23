import pytest

from src.algebra.number import Number
from src.algebra.restrictions.group import Group
from src.algebra.restrictions.ring import Ring


class TestNumber:

    @pytest.mark.parametrize(
        "test_value1,test_value2,modulo,expected",
        zip(
            [12, 54, 32, 12, 65, 11, 44, 23],
            [65, 88, 43, 33, 1443, 32, 123, -43],
            [11, 54, 64, 34, 76, 55, 12, 77],
            [0, 34, 11, 11, 64, 43, 11, 57],
        ),
    )
    def test_add(self, test_value1: int, test_value2: int, modulo: int, expected: int) -> None:
        result1: Number = Number(test_value1, Ring(modulo)) + Number(
            test_value2, Ring(modulo)
        )
        result2: Number = Number(test_value1, Group(modulo)) + Number(
            test_value2, Group(modulo)
        )

        assert result1.value == expected
        assert result2.value == expected

        result1 = Number(test_value2, Ring(modulo)) + Number(test_value1, Ring(modulo))
        result2 = Number(test_value2, Group(modulo)) + Number(
            test_value1, Group(modulo)
        )
        assert result1.value == expected
        assert result2.value == expected

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
        result: Number = Number(test_value1, Ring(modulo)) * Number(
            test_value2, Ring(modulo)
        )
        assert result.value == expected

        result = Number(test_value2, Ring(modulo)) * Number(test_value1, Ring(modulo))
        assert result.value == expected

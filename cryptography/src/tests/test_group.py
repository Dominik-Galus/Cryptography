import pytest

from cryptography.src.algebra.restrictions.group import Group


class TestGroup:

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
        group = Group(modulo)
        result = group.add(test_value1, test_value2)
        assert result == expected

    @pytest.mark.parametrize(
        "test_value, modulo, expected",
        [
            (35, 55, 20),
            (1000, 780, 560),
            (91, 12, 5),
            (387472, 12394, 9136),
            (758494, 239483, 199438),
            (9765, 1000, 235),
        ],
    )
    def test_add_inv(self, test_value: int, modulo: int, expected: int) -> None:
        group = Group(modulo)
        result = group.additive_inverse(test_value)
        assert result == expected

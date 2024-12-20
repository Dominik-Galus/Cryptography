import pytest

from cryptography.algebra.restrictions.field import Field


class TestField:

    @pytest.mark.parametrize(
        "test_value1, test_value2, modulo, expected",
        [
            (35, 99, 59, 23),
            (1000, 543, 787, 770),
            (92, 965, 13, 9),
            (387472, 6955486, 12391, 12224),
            (758494, 923444, 239489, 238898),
            (9765, 12385534, 1009, 80),
        ],
    )
    def test_division(
        self, test_value1: int, test_value2: int, modulo: int, expected: int,
    ) -> None:
        field = Field(modulo)
        result = field.division(test_value1, test_value2)
        assert result == expected

import pytest

from lotto_lab.validators.number_validator import validate_numbers


@pytest.mark.parametrize(
    "numbers",
    [[1, 2, 3, 4, 5, 49], [49, 35, 28, 21, 14, 7]],
)
def test_valid_lottery_numbers(numbers: list[int]) -> None:
    assert validate_numbers(numbers) is True


def test_fewer_than_six_numbers() -> None:
    assert validate_numbers([1, 2, 3, 4, 5]) is False


def test_more_than_six_numbers() -> None:
    assert validate_numbers([1, 2, 3, 4, 5, 6, 7]) is False


def test_duplicate_numbers() -> None:
    assert validate_numbers([1, 2, 3, 4, 5, 5]) is False


def test_number_below_one() -> None:
    assert validate_numbers([0, 2, 3, 4, 5, 6]) is False


def test_number_above_forty_nine() -> None:
    assert validate_numbers([1, 2, 3, 4, 5, 50]) is False


def test_string_value() -> None:
    assert validate_numbers(["1", 2, 3, 4, 5, 6]) is False


def test_float_value() -> None:
    assert validate_numbers([1.0, 2, 3, 4, 5, 6]) is False

def test_true_value() -> None:
    assert validate_numbers([1, 2, 3, 4, 5, 6]) is False


@pytest.mark.parametrize("value", [True, False])
def test_boolean_value(value: bool) -> None:
    assert validate_numbers([value, 2, 3, 4, 5, 6]) is False

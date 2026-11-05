import pytest

from lotto_lab.transformers.number_transformer import transform_numbers

def test_transform_numbers():
    raw_numbers = ["26", "2", "49", "6", "34", "33"]

    expected = [2, 6, 26, 33, 34, 49]

    actual = transform_numbers(raw_numbers)

    assert actual == expected

def test_transform_numbers_invalid_input():
    raw_numbers = ["26", "2", "ABC", "6", "34", "33"]

    with pytest.raises(ValueError):
        transform_numbers(raw_numbers)
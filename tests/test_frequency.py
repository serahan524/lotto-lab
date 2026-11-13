from lotto_lab.analysis.frequency import (
    calculate_number_frequency,
    calculate_bonus_frequency,
    get_top_numbers
)

def test_frequency_empty_draws():
    result = calculate_number_frequency([])

    assert len(result) == 49
    assert result[1] == 0
    assert result[49] == 0


def test_frequency_with_draws():
    draws = [
        {
            "n1": 1, "n2": 7, "n3": 12,
            "n4": 23, "n5": 35, "n6": 48
        },
        {
            "n1": 1, "n2": 8, "n3": 12,
            "n4": 24, "n5": 36, "n6": 49
        }
    ]

    result = calculate_number_frequency(draws)

    assert result[1] == 2
    assert result[12] == 2
    assert result[10] == 0
    assert sum(result.values()) == 12


def test_bonus_frequency():
    draws = [
        {"bonus": 9},
        {"bonus": 15},
        {"bonus": 9},
    ]

    result = calculate_bonus_frequency(draws)

    assert result[9] == 2
    assert result[15] == 1
    assert sum(result.values()) == 3


def test_get_top_numbers():
    frequency = {
        1: 2,
        7: 1,
        13: 3,
        30: 5
    }

    result = get_top_numbers(frequency, limit=2)

    assert result == [(30, 5), (13, 3)]


def test_get_top_numbers_exclude_zero():
    frequency = {1: 0, 7: 1, 27: 2, 38: 0}

    result = get_top_numbers(
        frequency,
        limit=10,
        exclude_zero=True
    )

    assert result == [(27, 2), (7, 1)]
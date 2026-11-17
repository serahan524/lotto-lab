from lotto_lab.storage.sqlite_storage import get_all_draws
from lotto_lab.analysis.frequency import (
    calculate_number_frequency,
    calculate_bonus_frequency,
    get_top_numbers
)


def generate_frequency_report(db_path):
    draws = get_all_draws(db_path)

    if not draws:
        return {
            "number_frequency": {n: 0 for n in range(1, 50)},
            "bonus_frequency": {n: 0 for n in range(1, 50)},
            "top_main": [],
            "top_bonus": []
        }

    number_frequency = calculate_number_frequency(draws)
    bonus_frequency = calculate_bonus_frequency(draws)

    top_main = get_top_numbers(number_frequency, limit=10)
    top_bonus = get_top_numbers(bonus_frequency, limit=10, exclude_zero=True)

    return {
        "number_frequency": number_frequency,
        "bonus_frequency": bonus_frequency,
        "top_main": top_main,
        "top_bonus": top_bonus
        }
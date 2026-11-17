from unittest.mock import patch

from lotto_lab.analysis.report import generate_frequency_report
from lotto_lab.storage.sqlite_storage import (
    initialize_database,
    insert_draw,
)



def test_generate_frequency_report_empty_db(tmp_path):
    db_path = tmp_path / "test.db"
    initialize_database(db_path)

    report = generate_frequency_report(db_path)

    assert report["top_main"] == []
    assert report["top_bonus"] == []


def test_generate_frequency_report_with_draws():
    draws = [
        {
            "n1": 1, "n2": 7, "n3": 13,
            "n4": 20, "n5": 30, "n6": 49,
            "bonus": 27
        },
        {
            "n1": 1, "n2": 9, "n3": 13,
            "n4": 21, "n5": 30, "n6": 45,
            "bonus": 38
        }
    ]

    with patch(
        "lotto_lab.analysis.report.get_all_draws",
        return_value=draws
    ):
        report = generate_frequency_report("dummy.db")

    assert report["number_frequency"][13] == 2
    assert report["number_frequency"][30] == 2
    assert report["bonus_frequency"][27] == 1
    assert report["top_bonus"] == [(27, 1), (38, 1)]

    assert len(report["top_main"]) == 10

    assert report["top_main"] == sorted(
        report["top_main"],
        key=lambda item: item[1],
        reverse=True
    )

    assert all(
        count > 0
        for number, count in report["top_bonus"]
    )


def test_generate_frequency_report_with_sqlite(tmp_path):
    db_path = tmp_path / "test.db"
    initialize_database(db_path)

    draw = {
        "game": "Western 649",
        "draw_date": "2026-01-01",
        "numbers": [1, 7, 13, 20, 30, 49],
        "bonus": 27,
        "source": "test"
    }

    insert_draw(db_path, draw)

    report = generate_frequency_report(db_path)

    assert report["number_frequency"][13] == 1
    assert report["bonus_frequency"][27] == 1
    assert report["top_main"][0][1] == 1
    assert report["top_bonus"] == [(27, 1)]
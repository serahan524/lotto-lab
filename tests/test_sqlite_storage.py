import sqlite3
import pytest

from lotto_lab.storage.sqlite_storage import initialize_database


def test_initialize_database(tmp_path):
    db_path = tmp_path / "test_lotto.db"

    initialize_database(db_path)

    assert db_path.exists()

    with sqlite3.connect(db_path) as conn:
        result = conn.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'lottery_draws'
        """).fetchone()

    assert result is not None
    assert result[0] == "lottery_draws"

from lotto_lab.storage.sqlite_storage import (
    initialize_database,
    insert_draw,
)


def test_insert_new_draw(tmp_path):
    db_path = tmp_path / "test_lotto.db"
    initialize_database(db_path)

    draw = {
        "game": "western_649",
        "draw_date": "2026-08-29",
        "numbers": [2, 6, 26, 33, 34, 49],
        "bonus": 19,
        "source": "wclc_website"
    }

    result = insert_draw(db_path, draw)

    assert result == "inserted"

# The same data
def test_insert_duplicate_draw(tmp_path):
    db_path = tmp_path / "test_lotto.db"
    initialize_database(db_path)

    original_draw = {
        "game": "western_649",
        "draw_date": "2026-08-29",
        "numbers": [2, 6, 26, 33, 34, 49],
        "bonus": 19,
        "source": "wclc_website"
    }

    duplicate_draw = {
            "game": "western_649",
            "draw_date": "2026-08-29",
            "numbers": [2, 6, 26, 33, 34, 49],
            "bonus": 19,
            "source": "wclc_website"
        }
    
    assert insert_draw(db_path, original_draw) == "inserted"
    assert insert_draw(db_path, duplicate_draw) == "skipped"

# The same game and date, but different winning number 
def test_insert_conflicting_draw(tmp_path):
    db_path = tmp_path / "test_lotto.db"
    initialize_database(db_path)

    original_draw = {
            "game": "western_649",
            "draw_date": "2026-08-29",
            "numbers": [2, 6, 26, 33, 34, 49],
            "bonus": 19,
            "source": "wclc_website"
        }

    conflicting_draw = {
            "game": "western_649",
            "draw_date": "2026-08-29",
            "numbers": [2, 6, 26, 33, 45, 49],
            "bonus": 19,
            "source": "wclc_website"
        }

    assert insert_draw(db_path, original_draw) == "inserted"
    assert insert_draw(db_path, conflicting_draw) == "conflict"

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
                """
                SELECT n1, n2, n3, n4, n5, n6, bonus
                FROM lottery_draws
                WHERE game = ? AND draw_date = ?
                """,
                ("western_649", "2026-08-29")
            ).fetchall()

    assert len(rows) == 1
    assert rows[0] == (2, 6, 26, 33, 34, 49, 19)


# Throw error when the data didn't go through data validation step
def test_insert_invalid_number_rejected(tmp_path):
    db_path = tmp_path / "test_lotto.db"
    initialize_database(db_path)

    invalid_draw = {
        "game": "western_649",
        "draw_date": "2026-09-02",
        "numbers": [2, 6, 26, 33, 34, 99],
        "bonus": 19,
        "source": "test"
    }

    with pytest.raises(sqlite3.IntegrityError):
        insert_draw(db_path, invalid_draw)

@pytest.mark.parametrize(
    "numbers, bonus",
    [
        ([2, 6, 26, 33, 34, 99], 19),
        ([2, 2, 26, 33, 34, 49], 19),
        ([6, 2, 26, 33, 34, 49], 19),
        ([2, 6, 26, 33, 34, 49], 26),
        ([2, 6, 26, 33, 34, 49], 50),
    ]
)
def test_invalid_draw_rejected(tmp_path, numbers, bonus):
    db_path = tmp_path / "test_lotto.db"
    initialize_database(db_path)

    invalid_draw = {
        "game": "western_649",
        "draw_date": "2026-09-02",
        "numbers": numbers,
        "bonus": bonus,
        "source": "test"
    }

    with pytest.raises(sqlite3.IntegrityError):
        insert_draw(db_path, invalid_draw)
import pytest
import sqlite3
from pathlib import Path

from lotto_lab.orchestration import save_draws
from lotto_lab.orchestration import run_etl
from lotto_lab.storage.sqlite_storage import initialize_database


def test_save_new_draws(tmp_path):
    db_path = tmp_path / "test_lotto.db"
    initialize_database(db_path)

    draws = [
        {
            "game": "western_649",
            "draw_date": "2026-08-29",
            "numbers": [2, 6, 26, 33, 34, 49],
            "bonus": 19,
            "source": "test"
        },
        {
            "game": "western_649",
            "draw_date": "2026-09-02",
            "numbers": [3, 8, 12, 25, 37, 45],
            "bonus": 10,
            "source": "test"
        }
    ]

    result = save_draws(db_path, draws)

    assert result == {
        "inserted": 2,
        "skipped": 0,
        "conflict": 0,
        "error": 0
    }

def test_save_duplicate_draws(tmp_path):
    db_path = tmp_path / "test_lotto.db"
    initialize_database(db_path)

    draws = [
        {
            "game": "western_649",
            "draw_date": "2026-08-29",
            "numbers": [2, 6, 26, 33, 34, 49],
            "bonus": 19,
            "source": "test"
        },
        {
            "game": "western_649",
            "draw_date": "2026-09-02",
            "numbers": [3, 8, 12, 25, 37, 45],
            "bonus": 10,
            "source": "test"
        }
    ]

    first_result = save_draws(db_path, draws)
    second_result = save_draws(db_path, draws)

    assert first_result == {
            "inserted": 2,
            "skipped": 0,
            "conflict": 0,
            "error": 0
        }
    assert second_result == {
            "inserted": 0,
            "skipped": 2,
            "conflict": 0,
            "error": 0
        }

def test_save_conflicting_draws(tmp_path):
    db_path = tmp_path / "test_lotto.db"
    initialize_database(db_path)

    draws = [
        {
            "game": "western_649",
            "draw_date": "2026-08-29",
            "numbers": [2, 6, 26, 33, 34, 49],
            "bonus": 19,
            "source": "test"
        },
        {
            "game": "western_649",
            "draw_date": "2026-08-29",
            "numbers": [3, 8, 12, 25, 37, 45],
            "bonus": 10,
            "source": "test"
        }
    ]

    result = save_draws(db_path, draws)
    
    assert result == {
        "inserted": 1,
        "skipped": 0,
        "conflict": 1,
        "error": 0
    }

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


def test_save_draws_continues_after_error(tmp_path):
    db_path = tmp_path / "test_lotto.db"
    initialize_database(db_path)

    draws = [
        {
            "game": "western_649",
            "draw_date": "2026-08-29",
            "numbers": [2, 6, 26, 33, 34, 49],
            "bonus": 19,
            "source": "test"
        },
        {
            "game": "western_649",
            "draw_date": "2026-09-02",
            "numbers": [3, 8, 12, 25, 37, 99],
            "bonus": 10,
            "source": "test"
        },
        {
            "game": "western_649",
            "draw_date": "2026-09-05",
            "numbers": [1, 5, 14, 22, 38, 47],
            "bonus": 9,
            "source": "test"
        }
    ]

    result = save_draws(db_path, draws)
        
    assert result == {
        "inserted": 2,
        "skipped": 0,
        "conflict": 0,
        "error": 1
    }

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT draw_date
            FROM lottery_draws
            ORDER BY draw_date
            """
        ).fetchall()

    assert rows == [
        ("2026-08-29",),
        ("2026-09-05",)
    ]   


def test_save_draws_stops_on_operational_error(monkeypatch):

    def fake_insert_draw(db_path, draw):
        raise sqlite3.OperationalError("database is locked")

    monkeypatch.setattr(
        "lotto_lab.orchestration.insert_draw",
        fake_insert_draw
    )

    draws = [
        {
            "game": "western_649",
            "draw_date": "2026-08-29",
            "numbers": [2, 6, 26, 33, 34, 49],
            "bonus": 19,
            "source": "test"
        }
    ]

    with pytest.raises(sqlite3.OperationalError):
        save_draws("dummy.db", draws)


def test_run_etl_end_to_end(tmp_path):
    fixture_path = (
        Path(__file__).parent
        / "fixtures"
        / "western_649_sample.html"
    )

    html = fixture_path.read_text(encoding="utf-8")
    db_path = tmp_path / "lotto.db"

    result = run_etl(html, db_path)

    assert result["storage"]["inserted"] == 2
    assert result["storage"]["error"] == 0


def test_run_etl_idempotency(tmp_path):
    fixture_path = (
        Path(__file__).parent
        / "fixtures"
        / "western_649_sample.html"
    )

    html = fixture_path.read_text(encoding="utf-8")
    db_path = tmp_path / "lotto.db"

    first_result = run_etl(html, db_path)
    second_result = run_etl(html, db_path)

    assert first_result["storage"]["inserted"] == 2
    assert first_result["storage"]["error"] == 0
    assert second_result["storage"]["inserted"] == 0
    assert second_result["storage"]["error"] == 0
    assert second_result["storage"]["skipped"] == 2
    assert second_result["storage"]["conflict"] == 0

    with sqlite3.connect(db_path) as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM lottery_draws"
        ).fetchone()[0]

    assert count == 2
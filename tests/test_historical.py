import sqlite3

from unittest.mock import patch

from lotto_lab.historical import collect_history
from lotto_lab.orchestration import save_draws


def test_collect_history_fetch_failure(tmp_path):
    db_path = tmp_path / "historical_test.db"

    with patch("lotto_lab.historical.fetch_html") as mock_fetch:
        mock_fetch.side_effect = ValueError("Simulated fetch failure")

        result = collect_history(db_path, 1)

    assert result["successful_months"] == []
    assert result["failed_months"][0]["back"] == 0
    assert result["failed_months"][0]["reason"] == "Simulated fetch failure"


def test_collect_history_continues_after_failure(tmp_path):
    db_path = tmp_path / "historical_test.db"

    storage_results = []

    def track_save(db_path, draws):
        result = save_draws(db_path, draws)
        storage_results.append(result)
        return result
    
    with (
        patch("lotto_lab.historical.fetch_html") as mock_fetch,
        patch("lotto_lab.historical.process_draws") as mock_process,
        patch("lotto_lab.historical.save_draws", wraps=track_save) as mock_save
    ):
        mock_fetch.side_effect = [
            ValueError("Simulated fetch failure"),
            "<html>Mock data</html>",
            ValueError("Simulated fetch failure"),
            "<html>Mock data</html>"
        ]

        mock_process.return_value = {
            "valid_draws": [
                {
                    "game": "Western 649",
                    "draw_date": "2026-09-30",
                    "numbers": [1, 7, 12, 23, 35, 48],
                    "bonus": 9,
                    "source": "WCLC"
                }
            ],
            "errors": []
        }

        result = collect_history(db_path, 2)

        with sqlite3.connect(db_path) as conn:
            first_count = conn.execute(
                "SELECT COUNT(*) FROM lottery_draws"
            ).fetchone()[0]

        second_result = collect_history(db_path, 2)

        with sqlite3.connect(db_path) as conn:
            second_count = conn.execute(
                "SELECT COUNT(*) FROM lottery_draws"
            ).fetchone()[0]

    assert result["successful_months"] == [1]
    assert result["failed_months"][0]["back"] == 0
    assert result["failed_months"][0]["reason"] == "Simulated fetch failure"
    assert second_result["successful_months"] == [1]

    assert mock_fetch.call_count == 4
    assert mock_process.call_count == 2
    assert mock_save.call_count == 2

    assert first_count == 1
    assert second_count == 1

    assert len(storage_results) == 2
    assert storage_results[0]["inserted"] == 1
    assert storage_results[1]["skipped"] == 1
    assert storage_results[1]["conflict"] == 0
    assert storage_results[1]["error"] == 0

    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT COUNT(*) FROM lottery_draws"
        ).fetchone()

    assert row[0] == 1


def determine_storage_status(storage_result):
    if storage_result["conflict"] == 0 and storage_result["error"] == 0:
        return "success"

    return "failed"

    
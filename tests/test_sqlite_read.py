from lotto_lab.storage.sqlite_storage import (
    initialize_database,
    insert_draw,
    get_all_draws,
)


def test_get_all_draws_empty(tmp_path):
    db_path = tmp_path / "test_read.db"

    initialize_database(db_path)

    result = get_all_draws(db_path)

    assert result == []


def test_get_all_draws_with_data(tmp_path):
    db_path = tmp_path / "test_read_with_data.db"
    initialize_database(db_path)

    draw = {
        "game": "Western 649",
        "draw_date": "2026-09-30",
        "numbers": [1, 7, 12, 23, 35, 48],
        "bonus": 9,
        "source": "WCLC"
    }

    insert_draw(db_path, draw)

    result = get_all_draws(db_path)

    assert len(result) == 1
    assert result[0]["draw_date"] == "2026-09-30"
    assert result[0]["n1"] == 1
    assert result[0]["n6"] == 48
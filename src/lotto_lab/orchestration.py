from pathlib import Path
from lotto_lab.storage.sqlite_storage import insert_draw


def save_draws(db_path: str | Path, draws: list[dict]) -> dict:
    results = {
        "inserted": 0, 
        "skipped": 0,
        "conflict": 0
    }

    
    return results
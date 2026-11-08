import sqlite3
from pathlib import Path
from lotto_lab.storage.sqlite_storage import insert_draw
from lotto_lab.storage.sqlite_storage import initialize_database
from lotto_lab.pipeline import process_draws


def save_draws(db_path: str | Path, draws: list[dict]) -> dict:
    results = {
        "inserted": 0, 
        "skipped": 0,
        "conflict": 0,
        "error": 0
    }

    for draw in draws: 
        try: 
            status = insert_draw(db_path, draw)        
            results[status] += 1

        except sqlite3.IntegrityError: 
            results["error"] += 1

    return results


def run_etl(html: str, db_path: str | Path) -> dict:
    initialize_database(db_path)
    processed = process_draws(html)
    save_result = save_draws(db_path, processed["valid_draws"])
        

    return {
            "processing": processed,
            "storage": save_result
        }


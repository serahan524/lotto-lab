import sqlite3
from pathlib import Path
from contextlib import closing


def initialize_database(db_path: str | Path) -> None:
    with closing(sqlite3.connect(db_path)) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS lottery_draws (
                draw_id INTEGER PRIMARY KEY,
                game TEXT NOT NULL,
                draw_date TEXT NOT NULL,

                n1 INTEGER NOT NULL CHECK (n1 BETWEEN 1 AND 49),
                n2 INTEGER NOT NULL CHECK (n2 BETWEEN 1 AND 49),
                n3 INTEGER NOT NULL CHECK (n3 BETWEEN 1 AND 49),
                n4 INTEGER NOT NULL CHECK (n4 BETWEEN 1 AND 49),
                n5 INTEGER NOT NULL CHECK (n5 BETWEEN 1 AND 49),
                n6 INTEGER NOT NULL CHECK (n6 BETWEEN 1 AND 49),

                bonus INTEGER NOT NULL CHECK (bonus BETWEEN 1 AND 49),
                source TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                UNIQUE (game, draw_date),
                CHECK (
                    n1 < n2 AND
                    n2 < n3 AND
                    n3 < n4 AND
                    n4 < n5 AND
                    n5 < n6
                ),
                CHECK (bonus NOT IN (n1, n2, n3, n4, n5, n6))
            )
        """)


def insert_draw(db_path: str | Path, draw: dict) -> str:
    with closing(sqlite3.connect(db_path)) as conn:
        with conn: 
            existing = conn.execute(
                """
                SELECT n1, n2, n3, n4, n5, n6, bonus
                FROM lottery_draws
                WHERE game = ? AND draw_date = ?
                """,
                (draw["game"], draw["draw_date"])
            ).fetchone()

            if existing is None:
                numbers = draw["numbers"]

                conn.execute(
                    """
                    INSERT INTO lottery_draws (
                        game, draw_date,
                        n1, n2, n3, n4, n5, n6,
                        bonus, source
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        draw["game"],
                        draw["draw_date"],
                        numbers[0],
                        numbers[1],
                        numbers[2],
                        numbers[3],
                        numbers[4],
                        numbers[5],
                        draw["bonus"],
                        draw["source"]
                    )
                )

                return "inserted"

            
            same_numbers = existing[:6] == tuple(draw["numbers"])
            same_bonus = existing[6] == draw["bonus"]

            if same_numbers and same_bonus:
                return "skipped"
            
            return "conflict"
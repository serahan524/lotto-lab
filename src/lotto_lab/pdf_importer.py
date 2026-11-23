import pdfplumber
import calendar
import re
from datetime import datetime
import sqlite3

from lotto_lab.storage.sqlite_storage import insert_draw


def extract_pdf_text(pdf_path):
    page_texts = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                # TODO 1: page_texts에 text 추가
                page_texts.append(text)

    # TODO 2: 페이지별 텍스트를 줄바꿈으로 연결
    full_text = "\n".join(page_texts)

    return full_text


def parse_draw_line(line):
    match = re.match(
        r"^([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})\s+",
        line
    )

    if not match:
        raise ValueError(f"Invalid date format: {line}")

    month, day, year = match.groups()

    date_text = f"{month} {day}, {year}"

    draw_date = datetime.strptime(
        date_text, "%B %d, %Y"
    ).strftime("%Y-%m-%d")

    remaining_text = line[match.end():]
    parts = remaining_text.split()

    if len(parts) < 7:
        raise ValueError("Invalid number count")

    numbers = [int(part) for part in parts[:6]]
    bonus = int(parts[6])

    if len(numbers) != len(set(numbers)):
        raise ValueError("Duplicate main numbers")

    if not all(1 <= number <= 49 for number in numbers):
        raise ValueError("Main number out of range")

    if not (1 <= bonus <= 49):
        raise ValueError("Bonus number out of range")

    if bonus in numbers:
        raise ValueError("Bonus duplicates main number")

    numbers = sorted(numbers)

    return {
        "game": "Western 649",
        "draw_date": draw_date,
        "numbers": numbers,
        "bonus": bonus,
        "source": "WCLC PDF"
    }


def parse_pdf_text(text):
    draws = []
    errors = []

    months = tuple(calendar.month_name[1:])

    for line in text.splitlines():
        line = line.strip()

        if not re.match(r"^[A-Za-z]+\s+\d{1,2},\s*\d{4}\b", line):
            continue

        try:
            draw = parse_draw_line(line)
            draws.append(draw)

        except ValueError as error:
            errors.append({
                "line": line,
                "error": str(error)
            })

    return {
        "valid_draws": draws,
        "errors": errors
    }


def save_pdf_draws(db_path, draws):
    counts = {
        "inserted": 0,
        "skipped": 0,
        "conflict": 0
    }

    for draw in draws:
        try:
            result = insert_draw(db_path, draw)
            counts[result] += 1

        except sqlite3.IntegrityError as error:
            raise ValueError(
                f"Failed to save draw: {draw}"
            ) from error

    return counts


def reconcile_draws(pdf_draws, db_draws):
    db_by_date = {
        draw["draw_date"]: draw
        for draw in db_draws
    }

    mismatches = []

    for pdf_draw in pdf_draws:
        draw_date = pdf_draw["draw_date"]
        db_draw = db_by_date.get(draw_date)

        if db_draw is None:
            mismatches.append({
                "draw_date": draw_date,
                "reason": "missing_in_db"
            })
            continue

        pdf_numbers = pdf_draw["numbers"]
        db_numbers = [db_draw[f"n{i}"] for i in range(1, 7)]

        if pdf_numbers != db_numbers or pdf_draw["bonus"] != db_draw["bonus"]:
            mismatches.append({
                "draw_date": draw_date,
                "reason": "number_mismatch",
                "pdf_numbers": pdf_numbers,
                "db_numbers": db_numbers
            })

    return mismatches
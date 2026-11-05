from pathlib import Path
from lotto_lab.pipeline import process_draws


def test_process_draws_valid_html():
    fixture_path = (
        Path(__file__).parent
        / "fixtures"
        / "western_649_sample.html"
    )

    html = fixture_path.read_text(encoding="utf-8")
    result = process_draws(html)

    assert len(result["valid_draws"]) == 2
    assert len(result["errors"]) == 0

def test_process_draws_invalid_numbers(monkeypatch):
    raw_draws = [
        {
            "raw_date": "Saturday, August 29, 2026",
            "raw_numbers": ["2", "6", "26", "33", "33", "49"],
            "raw_bonus": "19"
        }
    ]

    monkeypatch.setattr(
        "lotto_lab.pipeline.parse_draws",
        lambda html: {
            "raw_draws": raw_draws,
            "parse_errors": []
        }
    )   

    result = process_draws("<html></html>")

    assert len(result["valid_draws"]) == 0
    assert len(result["errors"]) == 1
    assert result["errors"][0]["reason"] == "Invalid main numbers or bonus"

def test_process_draws_invalid_bonus_format(monkeypatch):
    raw_draws = [
        {
            "raw_date": "Saturday, August 29, 2026",
            "raw_numbers": ["2", "6", "26", "33", "34", "49"],
            "raw_bonus": "ABC"
        }
    ]

    monkeypatch.setattr(
        "lotto_lab.pipeline.parse_draws",
        lambda html: {
            "raw_draws": raw_draws,
            "parse_errors": []
        }
    )

    result = process_draws("<html></html>")

    assert len(result["valid_draws"]) == 0
    assert len(result["errors"]) == 1
    assert "invalid literal" in result["errors"][0]["reason"]

def test_process_draws_continues_after_error(monkeypatch):
    raw_draws = [
        {
            "raw_date": "Saturday, August 29, 2026",
            "raw_numbers": ["2", "6", "26", "33", "34", "49"],
            "raw_bonus": "19"
        },
        {
            "raw_date": "Wednesday, August 26, 2026",
            "raw_numbers": ["3", "8", "12", "21", "35", "47"],
            "raw_bonus": "ABC"
        },
        {
            "raw_date": "Saturday, August 22, 2026",
            "raw_numbers": ["1", "9", "15", "28", "37", "44"],
            "raw_bonus": "11"
        }
    ]

    monkeypatch.setattr(
        "lotto_lab.pipeline.parse_draws",
        lambda html: {
            "raw_draws": raw_draws,
            "parse_errors": []
        }
    )

    result = process_draws("<html></html>")

    assert len(result["valid_draws"]) == 2
    assert len(result["errors"]) == 1
    assert result["valid_draws"][0]["draw_date"] == "2026-08-29"
    assert result["valid_draws"][1]["draw_date"] == "2026-08-22"
    assert result["errors"][0]["raw_date"] == "Wednesday, August 26, 2026"

def test_process_draws_includes_parser_errors(monkeypatch):
    raw_draws = [
        {
            "raw_date": "Saturday, August 29, 2026",
            "raw_numbers": ["2", "6", "26", "33", "34", "49"],
            "raw_bonus": "19"
        }
    ]
    monkeypatch.setattr(
            "lotto_lab.pipeline.parse_draws",
            lambda html: {
                "raw_draws": raw_draws,
                "parse_errors": [
            {
                "raw_date": "Wednesday, August 26, 2026",
                "reason": "Missing bonus tag"
            }
        ]
            }
        )
    result = process_draws("<html></html>")

    assert len(result["valid_draws"]) == 1
    assert len(result["errors"]) == 1
    assert "Missing bonus tag" in result["errors"][0]["reason"]
    assert result["errors"][0]["raw_date"] == "Wednesday, August 26, 2026"

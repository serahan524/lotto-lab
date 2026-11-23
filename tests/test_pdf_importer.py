import pytest

from lotto_lab.pdf_importer import (
    reconcile_draws,
    parse_draw_line,
    parse_pdf_text
)


@pytest.fixture
def sample_pdf_draws():
    return [
        {
            "draw_date": "2025-07-02",
            "numbers": [9, 14, 17, 20, 21, 43],
            "bonus": 5
        }
    ]

@pytest.fixture
def sample_db_draws():
    return [
        {
            "draw_date": "2025-07-02",
            "n1": 9,
            "n2": 14,
            "n3": 17,
            "n4": 20,
            "n5": 21,
            "n6": 43,
            "bonus": 5
        }
    ]


def test_reconcile_draws_matching_data(sample_pdf_draws, sample_db_draws):
    assert sample_db_draws[0]["n6"] == 43

    result = reconcile_draws(sample_pdf_draws, sample_db_draws)

    assert result == []   


def test_reconcile_draws_number_mismatch(sample_pdf_draws, sample_db_draws):

    sample_db_draws[0]["n6"] = 44

    result = reconcile_draws(sample_pdf_draws, sample_db_draws)

    assert len(result) == 1
    assert result[0]["reason"] == "number_mismatch"


def test_reconcile_draws_missing_in_db(sample_pdf_draws):
    db_draws = []

    result = reconcile_draws(sample_pdf_draws, db_draws)

    assert len(result) == 1
    assert result[0]["reason"] == "missing_in_db"
    assert result[0]["draw_date"] == "2025-07-02"


def test_parse_draw_line_valid():
    line = "July 2, 2025 14 17 20 21 9 43 5 1234567 EXTRA"

    result = parse_draw_line(line)

    assert result["draw_date"] == "2025-07-02"
    assert result["numbers"] == [9, 14, 17, 20, 21, 43]
    assert result["bonus"] == 5


"""
def test_parse_draw_line_invalid_number():
    line = "September 9, 2026 2 10 17 34 369 48 4 6728858 EXTRA"

    with pytest.raises(ValueError, match="Main number out of range"):
        parse_draw_line(line)


def test_parse_draw_line_duplicate_numbers():
    line = "July 2, 2025 9 14 17 20 21 21 5 1234567 EXTRA"

    with pytest.raises(ValueError, match="Duplicate main numbers"):
        parse_draw_line(line)


def test_parse_draw_line_missing_numbers():
    line = "July 2, 2025 9 14 17"

    with pytest.raises(ValueError, match="Invalid number count"):
        parse_draw_line(line)

"""


def test_parse_pdf_text_mixed_data():
    text = """
        July 2, 2025 14 17 20 21 9 43 5
        September 9, 2026 2 10 17 34 369 48 4
        July 5, 2025 1 8 12 25 33 49 7
        """

    result = parse_pdf_text(text)

    assert len(result["valid_draws"]) == 2
    assert len(result["errors"]) == 1
    
    assert "369" in result["errors"][0]["line"]
    assert result["errors"][0]["error"] == "Main number out of range"
    
    assert result["valid_draws"][0]["draw_date"] == "2025-07-02"
    assert result["valid_draws"][0]["numbers"] == [9, 14, 17, 20, 21, 43]

    assert result["valid_draws"][1]["draw_date"] == "2025-07-05"


@pytest.mark.parametrize(
    "line, expected_error",
    [
        (
            "July 2, 2025 9 14 17 20 21 21 5",
            "Duplicate main numbers"
        ),
        (
            "September 9, 2026 2 10 17 34 369 48 4",
            "Main number out of range"
        ),
        (
            "July 2, 2025 9 14 17",
            "Invalid number count"
        ),
    ]
)


def test_parse_draw_line_invalid_inputs(line, expected_error):
    with pytest.raises(ValueError, match=expected_error):
        parse_draw_line(line)



def test_parse_pdf_text_invalid_month():
    text = "Julu 2, 2025 9 14 17 20 21 43 5"

    result = parse_pdf_text(text)

    assert len(result["valid_draws"]) == 0
    assert len(result["errors"]) == 1


def test_parse_pdf_text_ignores_headers():
    text = """
    WESTERN 649 Since Inception
    Page 1 of 65
    July 2, 2025 14 17 20 21 9 43 5
    """

    result = parse_pdf_text(text)

    assert len(result["valid_draws"]) == 1
    assert len(result["errors"]) == 0
    assert result["valid_draws"][0]["draw_date"] == "2025-07-02"
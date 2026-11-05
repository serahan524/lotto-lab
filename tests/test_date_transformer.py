import pytest

from lotto_lab.transformers.date_transformer import transform_date


def test_transform_date_valid_wclc_date() -> None:
    assert transform_date("Saturday, August 29, 2026") == "2026-08-29"


def test_transform_date_invalid_day() -> None:
    with pytest.raises(ValueError):
        transform_date("Saturday, August 99, 2026")


def test_transform_date_invalid_format() -> None:
    with pytest.raises(ValueError):
        transform_date("2026/08/29")

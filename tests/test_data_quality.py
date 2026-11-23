from lotto_lab.analysis.data_quality import calculate_quality_metrics


def test_calculate_quality_metrics():
    result = {
        "valid_draws": [
            {"draw_date": "2025-07-02"},
            {"draw_date": "2025-07-05"},
        ],
        "errors": [
            {"error": "Main number out of range"},
        ],
    }

    metrics = calculate_quality_metrics(result)

    assert metrics["total_count"] == 3
    assert metrics["valid_count"] == 2
    assert metrics["error_count"] == 1
    assert metrics["pass_rate"] == 66.67
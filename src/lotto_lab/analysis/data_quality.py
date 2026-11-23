def calculate_quality_metrics(result):
    valid_count = len(result["valid_draws"])
    error_count = len(result["errors"])

    total_count = valid_count + error_count

    if total_count == 0:
        pass_rate = 0.0
    else:
        pass_rate = valid_count / total_count * 100

    return {
        "total_count": total_count,
        "valid_count": valid_count,
        "error_count": error_count,
        "pass_rate": round(pass_rate, 2),
    }
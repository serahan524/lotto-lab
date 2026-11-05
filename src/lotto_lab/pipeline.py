from lotto_lab.parsers.wclc_parser import parse_draws
from lotto_lab.transformers.date_transformer import transform_date
from lotto_lab.transformers.number_transformer import transform_numbers
from lotto_lab.validators.number_validator import validate_numbers


def process_draws(html: str) -> dict:
    parsed_result = parse_draws(html)

    raw_draws = parsed_result["raw_draws"]
    parse_errors = parsed_result["parse_errors"]

    valid_draws = []
    errors = list(parse_errors)

    for raw_draw in raw_draws: 
        try:

            # Transform date
            draw_date = transform_date(raw_draw["raw_date"])
            # Transform numbers
            numbers = transform_numbers(raw_draw["raw_numbers"])
            # Transform bonus
            bonus = int(raw_draw["raw_bonus"])

            # Validate numbers
            valid_numbers = validate_numbers(numbers)

            # Validate bonus
            valid_bonus = (
                1 <= bonus <= 49
                and bonus not in numbers
            )

            # Build standardized record
            if valid_numbers and valid_bonus: 
                standardized_record = {
                    "game": "western_649",
                    "draw_date": draw_date,
                    "numbers": numbers,
                    "bonus": bonus,
                    "source": "wclc_website"
                }

                valid_draws.append(standardized_record)

            else: 
                errors.append({
                    "raw_date": raw_draw["raw_date"],
                    "reason": "Invalid main numbers or bonus"
                })

        except (ValueError, TypeError, KeyError) as e: 
            errors.append({
                "raw_date": raw_draw.get("raw_date"),
                "reason": str(e)
                })

    return {
        "valid_draws": valid_draws,
        "errors": errors
    }
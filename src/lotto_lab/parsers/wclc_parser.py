from bs4 import BeautifulSoup


def parse_draws(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    draws = soup.select(".pastWinNum")

    results = []
    parse_errors = []

    for draw in draws: 
        raw_date = None

        try:
            date_tag = draw.select_one(".pastWinNumDate h4")
            number_tag = draw.select(".pastWinNumber")
            bonus_tag = draw.select_one(".pastWinNumberBonusText")

            if date_tag is None: 
                raise ValueError("Missing date tag")

            raw_date = date_tag.get_text(strip=True)
            
            if bonus_tag is None: 
                raise ValueError("Missing bonus tag")

            raw_numbers = [
                tag.get_text(strip=True) for tag in number_tag 
            ]

            bonus_value = bonus_tag.next_sibling

            if not isinstance(bonus_value, str) or not bonus_value.strip():
                raise ValueError("Missing bonus value")

            raw_bonus = bonus_value.strip()

            record = {
                "raw_date": raw_date, 
                "raw_numbers": raw_numbers,
                "raw_bonus": raw_bonus
            }

            results.append(record)

        except (ValueError, AttributeError, TypeError) as e: 
            parse_errors.append({
                "raw_date": raw_date,
                "reason": str(e)
            })
              
    return {
        "raw_draws": results,
        "parse_errors": parse_errors
    }
    
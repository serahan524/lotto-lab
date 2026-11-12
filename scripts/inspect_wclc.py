from bs4 import BeautifulSoup
from collections import Counter

from lotto_lab.fetcher import fetch_html
from lotto_lab.pipeline import process_draws

URL = "https://www.wclc.com/winning-numbers/western-649-extra.htm"


def main():
    html = fetch_html(URL)
    soup = BeautifulSoup(html, "html.parser")

    # 1. Inspect actual HTML structure
    draws = soup.select(".pastWinNumGroup")

    print("Number of draw groups:", len(draws))

    for index, draw in enumerate(draws[:3], start=1):
        date = draw.select_one(".pastWinNumDate")
        numbers = draw.select(".pastWinNumber")
        bonus = draw.select_one(".pastWinNumberBonus")

        print(f"\nDraw {index}:")
        print("Date:", date.get_text(" ", strip=True) if date else None)
        print(
            "Numbers:",
            [number.get_text(strip=True) for number in numbers]
        )
        print(
            "Bonus:",
            bonus.get_text(" ", strip=True) if bonus else None
        )

    # 2. Validate with existing pipeline
    result = process_draws(html)

    print("\nPipeline results:")
    print("Valid draws:", len(result["valid_draws"]))
    print("Errors:", len(result["errors"]))

    for draw in result["valid_draws"][:3]:
        print(draw)

    for error in result["errors"][:3]:
        print("Error:", error)

    # 3. Inspect historical month links
    months = soup.select(".pastMonthYearWinners")

    print("\nNumber of month elements:", len(months))

    for month in months[:5]:
        print(month.prettify()[:500])


if __name__ == "__main__":
    main()
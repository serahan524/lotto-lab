from bs4 import BeautifulSoup

from lotto_lab.fetcher import fetch_html
from lotto_lab.pipeline import process_draws


BASE_URL = "https://www.wclc.com"
HISTORY_PATH = "/western-649-extra.htm?back=2"


def main():
    url = f"{BASE_URL}/western-649-extra.htm?back=0"

    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    print("HTML length:", len(html))
    print("Draw groups:", len(soup.select(".pastWinNumGroup")))
    print("Page text:")
    print(soup.get_text(" ", strip=True)[:500])

    print("\nFirst 500 HTML characters:")
    print(html[:500])

    result = process_draws(html)

    print("\nPipeline validation:")
    print("Valid draws:", len(result["valid_draws"]))
    print("Errors:", len(result["errors"]))

    for error in result["errors"][:3]:
        print("Error:", error)

    for draw in result["valid_draws"][:2]:
        print("Draw:", draw)


if __name__ == "__main__":
    main()
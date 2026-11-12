from pathlib import Path

from lotto_lab.orchestration import run_etl_from_url

URL = "https://www.wclc.com/winning-numbers/western-649-extra.htm"
DB_PATH = Path("data/western_649_live_test.db")


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    result = run_etl_from_url(URL, DB_PATH)

    print("Processing:", result["processing"])
    print("Storage:", result["storage"])


if __name__ == "__main__":
    main()
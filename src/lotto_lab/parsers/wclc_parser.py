from bs4 import BeautifulSoup
from datetime import datetime

def parser_draws(html: str):
    soup = BeautifulSoup(html, "html.parser")
    draws = soup.select(".pastWinNum")

    for draw in draws: 
        numbers = draw.select(".pastWinNumber")
        bonus_tag = draw.select_one(".pastWinNumberBonusText")
        date_tag = draw.select_one(".pastWinNumDate h4")
        
        raw_date = date_tag.get_text(strip=True)

        raw_numbers = [
            tag.get_text(strip=True) for tag in numbers 
        ]

        raw_bonus = bonus_tag.next_sibling.strip()

              
        print(raw_numbers, raw_bonus, raw_date)
    
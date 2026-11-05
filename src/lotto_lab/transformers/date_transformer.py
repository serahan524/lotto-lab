from datetime import datetime

def transform_date(raw_date: str) -> str: 
    parsed_date = datetime.strptime(
                raw_date, 
                "%A, %B %d, %Y"
            )
    
    return parsed_date.strftime("%Y-%m-%d")  
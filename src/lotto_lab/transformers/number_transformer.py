# Transform data from string to integer

def transform_numbers(raw_numbers: list[str]) -> list[int]:
    return sorted([int(n) for n in raw_numbers])

def calculate_number_frequency(draws):
    frequency = {}

    # initialize
    for number in range(1, 50):
        frequency[number] = 0

    # actual frequency 
    for draw in draws: 
        for i in range(1, 7):
            column = f"n{i}"
            number = draw[column]
            frequency[number] += 1

    return frequency

def calculate_bonus_frequency(draws):
    frequency = {}

    # initialize
    for number in range(1, 50):
        frequency[number] = 0

    # actual frequency 
    for draw in draws:     
        number = draw["bonus"]
        frequency[number] += 1

    return frequency


def get_top_numbers(frequency, limit=10, exclude_zero=False):
    data = frequency
    
    if exclude_zero:
        data = {
            number: count
            for number, count in frequency.items()
            if count > 0
        }

    sorted_items = sorted(
        data.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return sorted_items[:limit]
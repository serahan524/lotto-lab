def validate_numbers(numbers: list[int]) -> bool:
    """
    Validate Lotto 6/49 numbers.

    Rules:
    - Exactly 6 numbers
    - All numbers must be integers
    - Numbers must be between 1 and 49
    - No duplicates
    """

    # 1. Check number count
    if len(numbers) != 6:
        return False

    # 2. Check data types
    if not all(type(number) is int for number in numbers):
        return False

    # 3. Check number range
    if not all(1 <= number <= 49 for number in numbers):
        return False

    # 4. Check duplicates
    if len(set(numbers)) != 6:
        return False

    return True


        
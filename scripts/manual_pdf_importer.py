import re
import copy

from lotto_lab.pdf_importer import (
    extract_pdf_text,
    parse_draw_line,
    parse_pdf_text,
    save_pdf_draws,
    reconcile_draws
)
from lotto_lab.storage.sqlite_storage import (
    initialize_database,
    insert_draw,
    get_all_draws
)

# check what the pdf file looks like
"""
pdf_path = "data/raw/WESTERN 649 Since Inception.pdf"

text = extract_pdf_text(pdf_path)

print(text[:1000])
"""

# check to see the parse_draw_line comes back with proper type of outputs
"""
line = "February 10, 1999 2 15 18 39 40 42 6 256471 THE PLUS"

date_text, numbers, bonus = parse_draw_line(line)

print(date_text)
print(numbers)
print(bonus)
print(type(numbers))

"""

# check to get dictionary from parse_draw_line(line)
"""
line = "February 10, 1999 2 15 18 39 40 42 6 256471 THE PLUS"

draw = parse_draw_line(line)

print(draw)
print(type(draw))
"""

# review the wrong date format when it converted using re.match 
"""
line = "December 22,2001 5 10 20 30 40 49 7 123456 THE PLUS"

match = re.match(r"^([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})\s+", line)

print(match.groups())
"""

# test wrong date format
"""
lines = [
    "February 10, 1999 2 15 18 39 40 42 6 256471 THE PLUS",
    "December 22,2001 5 10 20 30 40 49 7 123456 THE PLUS"
]

for line in lines:
    draw = parse_draw_line(line)
    print(draw)
"""

# pull whole pdf file 
"""
pdf_path = "data/raw/WESTERN 649 Since Inception.pdf"

text = extract_pdf_text(pdf_path)
draws = parse_pdf_text(text)

print("Total draws:", len(draws))
print("First draw:", draws[0])
print("Last draw:", draws[-1])
"""

# negative test - duplicated number
"""
line = "February 10, 1999 2 15 18 39 40 40 6 256471 THE PLUS"

draw = parse_draw_line(line)
print(draw)
"""

# negative test - number out of range
"""
line = "February 10, 1999 2 15 18 39 40 50 6 256471 THE PLUS"

draw = parse_draw_line(line)
print(draw)
"""

# negative test - bonus number duplicated 
"""
line = "February 10, 1999 2 15 18 39 40 42 42 256471 THE PLUS"

draw = parse_draw_line(line)
print(draw)
"""

# Error handling - 2 correct data & 1 wrong data
"""
test_text = "
February 10, 1999 2 15 18 39 40 42 6 256471 THE PLUS
February 13, 1999 5 6 11 13 16 30 4 272849 THE PLUS
February 17, 1999 5 8 12 24 41 41 26 781323 THE PLUS
"

result = parse_pdf_text(test_text)

print("Valid draws:", len(result["valid_draws"]))
print("Errors:", len(result["errors"]))
print("Error details:", result["errors"])
"""

# Maybe final test - whole data 
"""
pdf_path = "data/raw/WESTERN 649 Since Inception.pdf"

text = extract_pdf_text(pdf_path)
result = parse_pdf_text(text)

valid_draws = result["valid_draws"]
errors = result["errors"]

print("Valid draws:", len(valid_draws))
print("Errors:", len(errors))

for error in errors[:5]:
    print(error)
"""

# check if any duplicate dates 
"""
pdf_path = "data/raw/WESTERN 649 Since Inception.pdf"

text = extract_pdf_text(pdf_path)
result = parse_pdf_text(text)

valid_draws = result["valid_draws"]
dates = [draw["draw_date"] for draw in valid_draws]

unique_dates = set(dates)

print("Total valid draws:", len(dates))
print("Unique dates:", len(unique_dates))
print("Duplicate count:", len(dates) - len(unique_dates))
"""

#what would be valid draw? 
"""
pdf_path = "data/raw/WESTERN 649 Since Inception.pdf"

text = extract_pdf_text(pdf_path)
result = parse_pdf_text(text)

valid_draws = result["valid_draws"]
db_path = "data/lotto_pdf_test.db"

initialize_database(db_path)

draw = valid_draws[0]

result = insert_draw(db_path, draw)

print("Insert result:", result)
"""

# test save_pdf_draws()

pdf_path = "data/raw/WESTERN 649 Since Inception.pdf"

text = extract_pdf_text(pdf_path)
result = parse_pdf_text(text)

valid_draws = result["valid_draws"]
db_path = "data/lotto_pdf_test.db"

counts = save_pdf_draws(db_path, valid_draws)

print("Save results:", counts)


# check if the data exist in database

saved_draws = get_all_draws(db_path)

print("Total saved draws:", len(saved_draws))
print("Expected draws:", len(valid_draws))
print("Counts match:", len(saved_draws) == len(valid_draws))


# check reconcile_draws() 

valid_draws = result["valid_draws"]
db_path = "data/lotto_pdf_test.db"
mismatches = reconcile_draws(valid_draws, saved_draws)

print("Mismatches:", len(mismatches))
print("Mismatch dates:", mismatches[:10])

# negative test - wrong data
test_db_draws = copy.deepcopy(saved_draws)

test_db_draws[0]["n1"] = 49
test_mismatches = reconcile_draws(valid_draws, test_db_draws)

print("Test mismatches:", len(test_mismatches))
print("Test mismatch dates:", test_mismatches)

# negative test - when data on certain date is missing
test_missing_draws = saved_draws[1:]

missing_results = reconcile_draws(valid_draws, test_missing_draws)

print("Missing count:", len(missing_results))
print("Missing details:", missing_results[:3])
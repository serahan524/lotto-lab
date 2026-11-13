from lotto_lab.analysis.report import generate_frequency_report
from lotto_lab.storage.sqlite_storage import get_all_draws

db_path = "data/western_649_live_test.db" 

report = generate_frequency_report(db_path)

print("TOP 10 Main:", report["top_main"])
print("TOP 10 Bonus:", report["top_bonus"])

print("Main numbers:", report["number_frequency"])
print("Bonus numbers:", report["bonus_frequency"])

# Total
draws = get_all_draws(db_path)

print("Total draws:", len(draws))
print("Main total:", sum(report["number_frequency"].values()))
print("Bonus total:", sum(report["bonus_frequency"].values()))
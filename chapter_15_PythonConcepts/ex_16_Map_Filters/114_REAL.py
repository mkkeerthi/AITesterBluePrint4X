# 114_REAL.py
# Practical filter() example from test automation: keeps only the "PASS"
# results out of a mixed list of test outcomes.
test_results = ["PASS", "FAIL", "PASS", "SKIP", "FAIL"]

pass_give = list(filter(lambda x: x == "PASS", test_results))
print(pass_give)

# More complex: build a small test summary and pull out each category at once.
from collections import Counter

counts = Counter(test_results)
print("summary:", dict(counts))
print(f"pass rate: {counts['PASS'] / len(test_results):.0%}")

categories = {
    "passed": lambda r: r == "PASS",
    "failed": lambda r: r == "FAIL",
    "skipped": lambda r: r == "SKIP",
}

for label, predicate in categories.items():
    print(f"{label:<8}", list(filter(predicate, test_results)))

# Uniform results from richer records (dicts) - filter on a field.
results = [
    {"name": "login", "status": "PASS", "duration": 1.2},
    {"name": "search", "status": "FAIL", "duration": 3.5},
    {"name": "checkout", "status": "PASS", "duration": 5.1},
]
failed = [r for r in results if r["status"] == "FAIL"]
slow = list(filter(lambda r: r["duration"] > 3, results))
print("failed:", [r["name"] for r in failed])
print("slow:", [r["name"] for r in slow])

# Combining filter and map: names of passing, fast tests.
names = list(map(lambda r: r["name"],
                 filter(lambda r: r["status"] == "PASS" and r["duration"] < 3, results)))
print("passing and fast:", names)
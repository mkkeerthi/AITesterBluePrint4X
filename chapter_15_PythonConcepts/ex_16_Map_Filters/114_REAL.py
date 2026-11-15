# 114_REAL.py
# Practical filter() example from test automation: keeps only the "PASS"
# results out of a mixed list of test outcomes.
test_results = ["PASS", "FAIL", "PASS", "SKIP", "FAIL"]

pass_give = list(filter(lambda x: x == "PASS", test_results))
print(pass_give)
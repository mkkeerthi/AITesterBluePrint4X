# 54_Test.py
# Simulates running automated test cases: loops test ids 1-5 and prints a
# "Running the test case" message for each.
for test_id in range(1,6):
    print("Running the test case : ",test_id)

# More complex: simulate a small test runner that records results and
# stops early if a critical test fails.
test_cases = [
    ("login", True),
    ("search", True),
    ("checkout", False),
    ("logout", True),
]

passed, failed = 0, 0
for test_id, (name, ok) in enumerate(test_cases, start=1):
    print(f"[{test_id}] Running {name} ... {'PASS' if ok else 'FAIL'}")
    if ok:
        passed += 1
    else:
        failed += 1
        if name == "checkout":
            print("Critical test failed - stopping the run")
            break

print(f"Summary: {passed} passed, {failed} failed of {len(test_cases)}")
# 005_Variable.py
# Demonstrates variables and dynamic typing: the same name (age) first holds an
# integer then a string, and reassigning a variable simply keeps the latest value.
age = 65
age = "Pramod"
# Dynamic Typed Language. - It can understand you are doing, want.
print(age)
pi = 3.14
name = "Pramod"
name = "Dutta"
print(name)

# More complex: keep counters and totals of different types at the same time.
test_results = {
    "passed": 0,
    "failed": 0,
    "duration": 0.0,
}

scores = [88, 42, 91, 67]
for score in scores:
    if score >= 50:
        test_results["passed"] += 1
    else:
        test_results["failed"] += 1
    test_results["duration"] += 1.5

print(test_results)
print(f"Pass rate: {test_results['passed'] / len(scores) * 100:.1f}%")
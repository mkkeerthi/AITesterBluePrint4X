# 51_Loop.py
# for loop over range(0, 10, 1): prints the numbers 0 through 9 one per line.
# for i in range(1,10,1):
#     print(i)

# # 1 TO 9, -> 1

for i in range(0,10,1):
    print(i)

# More complex: accumulate values while looping, then report a summary.
total = 0
squares = []
for i in range(0, 10):
    total += i
    squares.append(i * i)

print("Sum 0-9:", total)
print("Squares:", squares)
print("Average:", total / 10)

# A loop that builds a formatted results table.
results = {"login": True, "search": False, "checkout": True}
passed = failed = 0
for test_name, ok in results.items():
    status = "PASS" if ok else "FAIL"
    passed += ok
    failed += not ok
    print(f"{test_name:<10} {status}")
print(f"{passed} passed, {failed} failed")
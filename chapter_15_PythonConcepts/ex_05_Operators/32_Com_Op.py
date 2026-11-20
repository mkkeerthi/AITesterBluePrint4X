# 32_Com_Op.py
# Demonstrates comparison operators (==, !=, >, <) which always return a boolean.
x, y = 10, 20
print(x == y)  # False
print(x != y)  # True
print(x > y)   # False
print(x < y)   # True

# More complex: the rest of the comparison operators, chained comparisons,
# and comparing different types.
print(x >= 10, x <= 10)     # True True
print(5 < x < 15)           # chained: same as 5 < x and x < 15
print("abc" == "abc", "abc" == "ABC")
print([1, 2] < [1, 3])      # lists compare element by element

# Comparisons return bool, which is also an int (True == 1).
print(x > y, int(x > y), (x > y) + 1)

# A realistic check: assert-style comparisons used in tests.
actual, expected = 200, 200
print(f"Status matches expected: {actual == expected}")

# Watch out: is compares identity, == compares value.
a = [1, 2]
b = [1, 2]
print(a == b, a is b)
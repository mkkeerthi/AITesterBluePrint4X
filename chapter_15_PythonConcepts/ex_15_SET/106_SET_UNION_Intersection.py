# 106_SET_UNION_Intersection.py
# Set algebra between {1,2,3} and {3,4,5}: union (|), intersection (&) and
# difference (-), each written with operators and their named method equivalents.
a = {1, 2, 3}
b = {3, 4, 5}

print(a | b)
print(a.union(b))

print(a & b)            # {3}
print(a.intersection(b))


print(a - b)

# More complex: the remaining set operators, the in-place versions, and a
# realistic "expected vs actual" comparison of test results.
print(a ^ b)                       # symmetric difference {1,2,4,5}
print(a.symmetric_difference(b))
print(a.difference(b))

c = {1, 2}
print("issubset:", c <= a)
print("superset:", a >= c)
print("disjoint:", a.isdisjoint({7, 8}))

# In-place variants mutate instead of returning a new set.
in_place = {1, 2, 3}
in_place &= {3, 4, 5}
print("after &=:", in_place)

# A realistic test-report comparison.
expected = {"login", "logout", "search"}
actual = {"login", "search", "checkout"}

print("Passed (both):", sorted(expected & actual))
print("Missing (never ran):", sorted(expected - actual))
print("Unexpected (new):", sorted(actual - expected))

# Multiple sets at once.
front, back, db = {1, 2, 3}, {2, 3, 4}, {3, 4, 5}
print("Union of three:", front | back | db)
print("Intersection of three:", front & back & db)
print("intersection() accepts several:", front.intersection(back, db))
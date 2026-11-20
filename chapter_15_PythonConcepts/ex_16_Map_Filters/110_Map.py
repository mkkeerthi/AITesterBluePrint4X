# 110_Map.py
# Introduces map(): applies a function (sq, which squares a number) to every
# element of a list and converts the lazy result into a list.
numbers = [1, 2, 3, 4, 5]
def sq(x):
    return x**2

# for n in numbers:
#     print(sq(n))

all_sq = list(map(sq, numbers))
print(all_sq)

# More complex: map with several iterables, map with None, and the lazy
# nature of map (it is an iterator, consumed once).
print("add pairwise:", list(map(lambda a, b: a + b, [1, 2, 3], [10, 20, 30])))
print("as strings:", list(map(str, numbers)))

# map stops at the shortest iterable when lengths differ.
print("uneven lengths:", list(map(lambda a, b: a * b, [1, 2, 3], [10, 20])))

# The result is an iterator - it can only be consumed once.
doubled = map(lambda n: n * 2, [1, 2, 3])
print(list(doubled))
print(list(doubled))   # empty the second time

# A list comprehension is usually more readable for a single transformation.
print("comprehension:", [n ** 2 for n in numbers])

# Realistic: convert raw dicts into clean records.
rows = [{"name": " pramod ", "score": "91"}, {"name": "amit ", "score": "47"}]
cleaned = list(map(lambda r: {"name": r["name"].strip(), "score": int(r["score"])}, rows))
print(cleaned)
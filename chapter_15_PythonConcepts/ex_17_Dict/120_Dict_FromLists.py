# 120_Dict_FromLists.py
# Builds a dictionary by pairing two lists with dict(zip(keys, values)) - extra
# values are ignored - then shows that dict equality does not depend on key order.
keys = ["name", "role", "experience", "abc"]
values = ["Aman", "SDET", 3, 67,90]
# values = ["Aman", "SDET"]

my_dict = dict(zip(keys, values))
print(my_dict)

dict1 = {"a": 1, "b": 2}
dict2 = {"b": 2, "a": 1}

print(dict1 == dict2)

# More complex: dict comprehensions, inverting a mapping, and sorting by value.
scores = {"pramod": 91, "amit": 47, "navita": 88}

squared = {name: score for name, score in scores.items()}
print(squared)

passed = {name: score for name, score in scores.items() if score >= 50}
print("passing:", passed)

# Invert a dict (values must be unique).
inverted = {score: name for name, score in scores.items()}
print(inverted)

# Visit keys in sorted order, and sort items by value.
print("sorted names:", sorted(scores))
for name, score in sorted(scores.items(), key=lambda item: item[1], reverse=True):
    print(f"{name:<8} {score}")

# zip stops at the shorter sequence, so a short values list drops keys.
print(dict(zip(["a", "b", "c"], [1, 2])))
# zip_longest can fill the gaps instead.
from itertools import zip_longest
print(dict(zip_longest(["a", "b", "c"], [1, 2], fillvalue=None)))

# Two lists of equal length make a clean mapping.
keys = ["host", "port", "user"]
values = ["localhost", 5432, "admin"]
config = dict(zip(keys, values))
print(config["port"], type(config["port"]))
# 104_SET.py
# Demonstrates that a set keeps only unique items: duplicates are removed
# automatically, and set() converts a list (with repeats) into a set.
# # SET
# # Collection of Unique
# # {} - parenthesis

list_of_unique_items = {1, 2, 3, 4, 4, 5, 5}
print(list_of_unique_items)


list1 = [45.2, 33, 33, 45, 21]
set1 = set(list1)
print(set1)

# More complex: deduplication while keeping the original order (a set alone
# does not preserve order), and counting occurrences with a dict.
items = ["b", "a", "b", "c", "a", "d"]
print("set order (unspecified):", set(items))
print("order preserved:", list(dict.fromkeys(items)))

counts = {}
for item in items:
    counts[item] = counts.get(item, 0) + 1
print("counts:", counts)
print("duplicated values:", [k for k, v in counts.items() if v > 1])

# Comparing two collections as sets is often the cleanest check.
expected = {"login", "search", "logout"}
actual = {"login", "logout", "search", "search"}
print("Same tests, any order:", set(actual) == expected)

# Sets are unordered, so never rely on the order of their output.
print("Set of mixed types:", {1, "1", 1.0})   # note 1 == 1.0
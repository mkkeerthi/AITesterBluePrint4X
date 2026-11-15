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
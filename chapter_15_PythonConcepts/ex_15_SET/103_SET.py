# 103_SET.py
# Introduces sets: unordered collections of unique values written with braces.
# Duplicate 3s in the second set are automatically collapsed to one.
my_set = {1, 2, 3}
print(my_set) 


my_set_2 = {1, 2, 3, 3}
print(my_set_2)

# More complex: a set has no order or index, so membership is the point.
numbers = {3, 1, 4, 1, 5, 9, 2, 6, 5}
print("Unique count:", len(numbers))
print("Is 4 present?", 4 in numbers)
print("Is 7 present?", 7 in numbers)
print("Sorted view:", sorted(numbers))   # sorting produces a list

# Adding and discarding is fast and idempotent.
numbers.add(7)
numbers.discard(3)      # no error if absent, unlike remove()
print("Updated:", sorted(numbers))

# A set cannot hold mutable items like lists - they are unhashable.
try:
    {[1, 2]}
except TypeError as error:
    print("TypeError:", error)

# Duplicate detection is a classic use.
names = ["pramod", "amit", "pramod", "navita"]
print("Duplicates exist:", len(names) != len(set(names)))
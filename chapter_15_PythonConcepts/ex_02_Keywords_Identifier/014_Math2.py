# 014_Math2.py
# Uses the built-in max() and min() functions to find the largest and
# smallest values in a list of numbers.
result = max(3, 4, 5, 100, 101)
print(result)


result_min = min(3, 4)
print(result_min)


result = max(3, 4, 67, -1, 190, 999, 100000, 9899, -1)
print(result)

# More complex: max()/min() on a list, with a key function, and with a default.
scores = [("Pramod", 91), ("Amit", 47), ("Navita", 88)]
print("Best:", max(scores))                    # compares tuples item by item
print("Best by score:", max(scores, key=lambda item: item[1]))
print("Worst by score:", min(scores, key=lambda item: item[1]))

# key lets you ignore case when comparing strings
words = ["banana", "Apple", "cherry"]
print("Max ignoring case:", max(words, key=str.lower))

# default= prevents ValueError when the iterable is empty
empty = []
print("Max with default:", max(empty, default="no data"))
print("Min with default:", min(empty, default="no data"))
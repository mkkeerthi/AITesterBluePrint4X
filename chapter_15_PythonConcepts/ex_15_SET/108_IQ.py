# 108_IQ.py
# Set comprehension: builds the set of squares of 0-4 in one line; duplicates
# would be dropped automatically as with any set.
squares = {x ** 2 for x in range(5)}
print(squares)


# 108_IQ.py
# Set comprehension: builds the set of squares of 0-4 in one line; duplicates
# would be dropped automatically as with any set.
squares = {x ** 2 for x in range(5)}
print(squares)


# More complex: a comprehension with a condition, and one over nested data.
print("Even squares:", {x ** 2 for x in range(10) if x % 2 == 0})

# A conditional expression inside the comprehension changes values, not membership.
print("Signed squares:", {x ** 2 if x % 2 == 0 else -x ** 2 for x in range(5)})

# Flattening a nested structure with a set comprehension.
records = [{"tags": ["smoke", "ui"]}, {"tags": ["ui", "api"]}]
all_tags = {tag for record in records for tag in record["tags"]}
print("Unique tags:", sorted(all_tags))

# Sets also have frozenset siblings - usable inside other sets or as dict keys.
print(frozenset([1, 2, 2, 3]))

# A dict comprehension produces a mapping, which is the natural next step.
word_lengths = {word: len(word) for word in ["qa", "automation", "test"]}
print(word_lengths)


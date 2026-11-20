# 107_IQ.py
# Builds a set from a list of strings, removes the duplicate entry, then shows
# the set's size with len() and iterates over its elements.
set1 = set(["TheTestingAcademy", "For", "TheTestingAcademy."])
print(set1)
print(len(set1))


for i in set1:
    print(i)

# More complex: word-level deduplication and a frequency count, which is a
# much more useful form of the same idea.
sentence = "the quick brown fox jumps over the lazy dog the end"
words = sentence.split()

print("All words:", len(words))
print("Unique words:", len(set(words)))
print("Duplicated words:", sorted({w for w in words if words.count(w) > 1}))

# Iterating a set gives unpredictable order - sort it when output matters.
for word in sorted(set(words)):
    print(word)

# Building a set incrementally while filtering.
long_words = set()
for word in words:
    if len(word) > 3:
        long_words.add(word)
print("Longer than 3 chars:", sorted(long_words))
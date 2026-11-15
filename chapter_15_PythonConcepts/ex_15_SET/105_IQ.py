# 105_IQ.py
# Converts a tuple with duplicates to a set to deduplicate it, creates an empty
# set with set(), and shows adding/removing items and iterating a mixed-type set.
t = ("TheTestingAcademy", "for", "TheTestingAcademy")
print(t)
print(set(t))

empty = set()
print(type(empty))


mixed = {1, "QA", True, 3.5}
for item in mixed:
    print(item)

mixed.add(10)
print(mixed)
mixed.remove(10)
print(mixed)
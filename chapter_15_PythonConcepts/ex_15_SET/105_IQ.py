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

# More complex: set operations for real work - difference to find missing
# values, union to combine, and issubset for coverage checks.
required = {"login", "search", "checkout"}
executed = {"login", "checkout"}

print("Not executed:", required - executed)
print("Executed too:", executed - required)
print("All tests:", required | executed)
print("Common:", required & executed)
print("Symmetric difference:", required ^ executed)

print("Executed covers all required?", required.issubset(executed))
print("No overlap?", required.isdisjoint({"payment"}))

# remove() raises KeyError for a missing value; discard() does not.
try:
    executed.remove("payment")
except KeyError as error:
    print("KeyError:", error)
executed.discard("payment")   # silent

# A set can be modified in place while keeping the same object.
executed |= {"payment"}
executed -= {"search"}
print("final:", sorted(executed))
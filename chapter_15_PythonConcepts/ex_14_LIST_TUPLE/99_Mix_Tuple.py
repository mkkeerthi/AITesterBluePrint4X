# 99_Mix_Tuple.py
# A tuple can hold mixed types (string, int, bool, float). Also shows that a
# one-element tuple needs a trailing comma: (3,) is a tuple, (3) is just an int.
info = ("Pramod", 34, True, 9.8)
print(info)

#Tuple with One Element
single=  (3,)
print(type(single))

# More complex: why the trailing comma matters, and nested/mixed tuples.
not_a_tuple = (3)
print(type(not_a_tuple).__name__, "-> parentheses alone are just grouping")

empty = ()
print("empty:", empty, type(empty).__name__)

# Nested tuples and a loop that shows each element's type.
record = ("pramod", 34, True, 9.8, ("python", "java"))
for value in record:
    print(f"{str(value):<24} {type(value).__name__}")

# Destructuring a nested tuple in one assignment.
name, age, active, rating, skills = record
print(name, age, active, rating, skills[0])

# Tuples support the same read operations as lists, plus hashability.
print("count of 'python' in skills:", skills.count("python"))
print("sliced:", record[:2])

# A tuple of tuples behaves like a read-only table.
rows = (("id", "name"), (1, "pramod"), (2, "amit"))
for row in rows:
    print(" | ".join(str(cell) for cell in row))
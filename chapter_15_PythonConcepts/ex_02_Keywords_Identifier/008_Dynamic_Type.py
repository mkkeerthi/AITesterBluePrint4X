# 008_Dynamic_Type.py
# Illustrates that Python is dynamically typed: the same variable can be
# reassigned to an int, a string and a bool, with type() showing the change.
# Dynamically typed

age = 98
print(type(age))
age = "Pramod"
print(type(age))
age = True
print(type(age))

# More complex: dynamic typing inside a function, plus isinstance checks
# to act safely on whatever type currently lives in the variable.
def show(value):
    if isinstance(value, bool):
        # bool is a subclass of int, so check bool first
        kind = "boolean"
    elif isinstance(value, int):
        kind = "integer"
    elif isinstance(value, (list, tuple, set, dict)):
        kind = f"container of {len(value)} items"
    else:
        kind = type(value).__name__
    print(f"{str(value):<20} is a {kind}")


for v in [10, 3.5, False, [1, 2, 3], {"a": 1}, "text"]:
    show(v)
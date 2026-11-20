# 39.py
# Stores the result of a not-equal comparison (x != y) in a variable and prints it.
x = 10
y = 20
result = (x != y)
print(result)

# More complex: store several comparison results and use them in decisions.
is_greater = x > y
is_equal = x == y
differ = x != y
print(is_greater, is_equal, differ)

# any()/all() combine a collection of booleans neatly.
checks = [is_greater, is_equal, differ]
print("Any true:", any(checks))
print("All true:", all(checks))

# A realistic validation: all conditions must hold.
data = {"name": "pramod", "age": 30, "email": "p@example.com"}
required = ["name", "email"]
valid = all(field in data and data[field] for field in required)
print("Record valid:", valid)
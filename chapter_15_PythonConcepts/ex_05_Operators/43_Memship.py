# 43_Memship.py
# Shows the membership operators in / not in for checking substrings, then
# uses the math module for pi and trigonometric/power functions.
result = 'a' in 'apple'
result2 = 'b' in 'apple'
result3 = 'b' not in 'apple'
print(result)
print(result2)
print(result3)

import math

print(math.pi)
print(math.pow(2, 2))
print(math.sin(90))
print(math.cos(90))
print(math.tan(90))

# More complex: membership in lists, dicts and sets, and a realistic
# "is this value allowed?" check.
allowed_methods = {"GET", "POST", "PUT", "DELETE"}
print("GET" in allowed_methods)
print("PATCH" in allowed_methods)

user = {"name": "pramod", "role": "admin"}
print("email" in user)          # dict membership checks KEYS
print("admin" in user.values()) # check values separately

# Combining membership with logical operators for a permission check.
role = "admin"
if role in {"admin", "owner"} and "DELETE" in allowed_methods:
    print("Delete permitted")

# math also has floor, ceil and sqrt - useful for pagination.
print(math.sqrt(16), math.floor(3.7), math.ceil(3.2))
print(math.isclose(0.1 + 0.2, 0.3))
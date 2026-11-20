# 19.py
# Creates a float literal and prints its type, then uses the built-in
# max() and min() functions to compare two integers.
gst = 18.45
print(type(gst))

result = max(45, 65)
result_min = min(45, 65)
print(result)
print(result_min)

# More complex: round a float price, and compare several floats carefully.
price = 1299.9876
print(round(price, 2))          # keep 2 decimals
print(round(price))             # nearest integer
print(type(round(price)))

# Floating-point values are binary fractions, so exact comparison can fail.
a = 0.1 + 0.2
b = 0.3
print(a)
print(a == b)                   # False - tiny rounding difference
print(abs(a - b) < 1e-9)        # True - compare within a tolerance

import math
print(math.isclose(a, b))
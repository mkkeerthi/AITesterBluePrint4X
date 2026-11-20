# 160_DivsionError.py
# Demonstrates a ZeroDivisionError raised by dividing an integer by zero.
try:
    print(10/0)
except ZeroDivisionError as error:
    print("ZeroDivisionError:", error)
# ZeroDivisionError

# More complex: the same failure caught, plus the integer vs float variants
# and the difference between / and //.
try:
    print(10 / 0)
except ZeroDivisionError as error:
    print("caught:", error)

try:
    print(10 // 0)          # floor division fails the same way for ints
except ZeroDivisionError as error:
    print("floor division:", error)

# Division by zero with floats also raises ZeroDivisionError in Python.
try:
    print(10 / 0.0)
except ZeroDivisionError as error:
    print("float division:", error)

# Only explicitly built infinities produce inf/nan instead of raising.
import math
positive_inf = float("inf")
nan_value = positive_inf - positive_inf
print("isinf:", math.isinf(positive_inf), "| isnan:", math.isnan(nan_value))

# A helper that returns a safe result instead of crashing.
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


for pair in [(10, 2), (10, 0), (0, 5)]:
    print(pair, "->", safe_divide(*pair))
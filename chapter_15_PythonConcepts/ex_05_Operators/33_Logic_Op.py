# 33_Logic_Op.py
# Demonstrates logical operators: and (both true), or (either true) and not (negation).
a, b = 5, 10
print(a > 0 and b > 0)  # True
print(a > 0 or b < 0)   # True
print(not (a > 0))      # False

# More complex: short-circuit behaviour and truthiness.
# and stops at the first falsy value, or stops at the first truthy value,
# and both return the VALUE, not necessarily a bool.
print(0 and "never runs")
print(0 or "fallback")
print("hello" and "world")

# Truthy/falsy values: empty containers and 0 are falsy.
for value in [0, 1, "", "x", [], [1], None]:
    print(f"{str(value):<6} -> {bool(value)}")

# Combining conditions the way a test would validate a response.
status = 200
body = {"user": "pramod"}
is_success = 200 <= status < 300 and bool(body)
print("Request succeeded:", is_success)

# not is often clearer than comparing to False.
is_ready = False
if not is_ready:
    print("Waiting for setup")
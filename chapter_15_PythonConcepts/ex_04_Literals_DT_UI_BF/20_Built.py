# 20_Built.py
# Introduces Python's built-in functions (provided by Python, no import needed):
# pow() for exponentiation and abs() for the absolute value.
# Built In - Functions
# Pre defind given by the Python guys to you to use it.

# max()
# min()
# print()
print(pow(2, 3))
b = abs(-10)  # Return the absolute value of the argument.
print(b)

# More complex: pow() with a modulus (used a lot in hashing/crypto) and
# a tour of other commonly used built-ins.
print(pow(2, 10, 1000))          # (2 ** 10) % 1000 = 1024 % 1000
print(divmod(17, 5))             # quotient and remainder in one call
print(sum([1, 2, 3, 4, 5]))
print(sorted([3, 1, 2], reverse=True))
print(round(3.14159, 3))
print(len("testing"))
print(list(enumerate(["a", "b"])))
print(bool(0), bool(1))

# A realistic combination: compare two latencies and report the difference.
measured = 245
threshold = 200
gap = abs(measured - threshold)
print(f"Over threshold by {gap} ms ({gap / threshold:.0%})")
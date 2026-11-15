# 166_Fix.py
# The "fix" version: the division is wrapped in try/except so a ZeroDivisionError
# is caught and a friendly message is printed instead of crashing the program.
a = int(input("Enter num 1"))
b = int(input("Enter num 2"))
try:
    c = a/b
    print(c)
except ZeroDivisionError:
    print("Error bue to ZDE")



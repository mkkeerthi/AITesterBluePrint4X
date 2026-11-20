# 165.py
# The "problem" version: reads two numbers and divides them with no error
# handling, so entering 0 as the second number raises ZeroDivisionError.
a = int(input("Enter num 1"))
b = int(input("Enter num 2"))
c = a/b
print(c)
# ZeroDivisionError: division by zero

# More complex: the same operation with full validation and error handling,
# so bad input never crashes the script.
def read_number(prompt, default):
    # input() is replaced with a default here so the file runs unattended.
    raw = str(default)
    try:
        return int(raw)
    except ValueError:
        print(f"{prompt}: '{raw}' is not a number")
        return None


def divide(a, b):
    if a is None or b is None:
        return "cannot divide: invalid input"
    if b == 0:
        return "cannot divide by zero"
    return round(a / b, 4)


cases = [(10, 2), (10, 0), ("x", 2), (7, 3)]
for first, second in cases:
    x = read_number("Enter num 1", first)
    y = read_number("Enter num 2", second)
    print(f"{first} / {second} -> {divide(x, y)}")
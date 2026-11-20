# 161_TypeError.py
# Demonstrates a TypeError: adding an int and a str is not allowed
# ("unsupported operand type(s)").
try:
    print( 1 + "1")
except TypeError as error:
    print("TypeError:", error)
# TypeError: unsupported operand type(s) for +: 'int' and 'str'

# More complex: catch it, fix it properly, and see the other common
# TypeErrors worth knowing.
try:
    print(1 + "1")
except TypeError as error:
    print("caught:", error)

print(1 + int("1"))         # explicit conversion
print(str(1) + "1")         # or make both strings

# Calling a non-callable and passing the wrong number of arguments are also
# TypeErrors.
not_callable = "text"
for bad_call in [lambda: not_callable(), lambda: len(), lambda: "abc" + 1]:
    try:
        bad_call()
    except TypeError as error:
        print("TypeError:", error)

# isinstance lets you branch instead of relying on exceptions.
def add(a, b):
    if isinstance(a, str) or isinstance(b, str):
        return f"{a}{b}"
    return a + b


print(add(1, "1"), add(1, 2))

# A realistic pattern: convert user input, report the failure clearly.
def to_number(raw, kind=int):
    try:
        return kind(raw)
    except (TypeError, ValueError) as error:
        return f"invalid ({type(error).__name__}: {error})"


print(to_number("42"), to_number(None), to_number("x"))

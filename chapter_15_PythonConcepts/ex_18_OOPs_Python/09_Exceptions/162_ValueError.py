# 162_ValueError.py
# Demonstrates a ValueError: int("a") cannot convert a non-numeric string.
try:
    print(int("a"))
except ValueError as error:
    print("ValueError:", error)
# ValueError: invalid literal for int() with base 10: 'a'

# More complex: catch the ValueError and convert several inputs safely, with
# defaults so the program keeps running.
for raw in ["10", "3.5", "a", "", "  12  ", "0x1f"]:
    try:
        print(f"{raw!r:<9} -> {int(raw)}")
    except ValueError as error:
        print(f"{raw!r:<9} -> ValueError: {error}")

# int() with a base parses other formats; float() accepts decimals, and an
# int() on a decimal string raises ValueError.
print(int("0x1f", 16), int("1010", 2), sep=" | ")
try:
    int("3.5")
except ValueError as error:
    print("int('3.5'):", error)
print(int(float("3.5")))         # two-step when a decimal string must be int

# A helper that always returns a usable number.
def parse_int(raw, default=0):
    try:
        return int(raw)
    except (TypeError, ValueError):
        return default


print(parse_int("42"), parse_int("nope"), parse_int(None, default=-1))

# ValueError also comes from range(), months and other builtins.
try:
    range(1, 2, 0)
except ValueError as error:
    print("range:", error)

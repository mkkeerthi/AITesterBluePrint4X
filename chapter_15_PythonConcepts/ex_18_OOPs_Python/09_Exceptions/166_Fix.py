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

# More complex: one block that handles both failure modes, reports them in a
# consistent way, and closes its resources with finally.
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError as error:
        print(f"  ZeroDivisionError: {error}")
        return None
    except TypeError as error:
        print(f"  TypeError: {error}")
        return None
    else:
        # Runs only when no exception was raised.
        print(f"  result: {result}")
        return result
    finally:
        # Always runs - good for logging or cleanup.
        print("  attempt finished")


for a, b in [(10, 2), (10, 0), ("10", 2)]:
    try:
        divide(int(a), int(b))
    except ValueError as error:
        print(f"  could not convert input: {error}")

# Catching multiple exception types in one clause.
try:
    value = int("abc") / 0
except (ValueError, ZeroDivisionError) as error:
    print(f"caught {type(error).__name__}: {error}")



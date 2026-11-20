# 168_Fix3.py
# Handles two possible failures separately: a non-numeric input raises
# ValueError and division by zero raises ZeroDivisionError; each has its own except block.
try:
    a = int(input("Enter num 1"))
    b = int(input("Enter num 2"))
    c = a / b
    print(c)
except ValueError:
    print("Value Error")
except ZeroDivisionError:
    print("Div Error")

# More complex: the same two handlers, driven by data so the file runs
# unattended, plus retry logic and exception chaining.
def attempt(a_raw, b_raw):
    try:
        a = int(a_raw)
        b = int(b_raw)
        return a / b
    except ValueError as error:
        print(f"ValueError: {error!r} for input {a_raw!r}/{b_raw!r}")
    except ZeroDivisionError as error:
        print(f"ZeroDivisionError: {error}")
    return None


for a_raw, b_raw in [("10", "2"), ("abc", "2"), ("10", "0"), ("10", "x")]:
    print(f"{a_raw}/{b_raw} -> {attempt(a_raw, b_raw)}")

# Retrying a flaky operation: stop at the first success or after N attempts.
def with_retries(fn, attempts=3):
    for attempt_number in range(1, attempts + 1):
        try:
            return fn(attempt_number)
        except ValueError as error:
            print(f"  attempt {attempt_number} failed: {error}")
    return "gave up"


def flaky(n):
    if n < 3:
        raise ValueError("not yet")
    return "succeeded"


print(with_retries(flaky))

# raise ... from ... keeps the original cause visible.
try:
    try:
        int("x")
    except ValueError as error:
        raise RuntimeError("could not parse the config") from error
except RuntimeError as error:
    print(f"{error} (caused by {type(error.__cause__).__name__})")
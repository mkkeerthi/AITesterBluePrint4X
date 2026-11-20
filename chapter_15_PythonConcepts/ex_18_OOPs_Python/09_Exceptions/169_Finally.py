# 169_Finally.py
# Adds finally to the try/except: the finally block runs no matter what, whether
# an exception was raised, caught, or no error occurred at all.
try:
    a = int(input("Enter num 1"))
    b = int(input("Enter num 2"))
    c = a / b
    print(c)
except ValueError:
    print("Value Error")
except ZeroDivisionError:
    print("Div Error")
finally:
    print("I will always execute!")

# More complex: finally as a guaranteed cleanup step, including when the
# exception is NOT caught, and comparing it with the `with` statement.
def run_uncaught():
    try:
        print("  opening a resource")
        raise RuntimeError("boom")
    finally:
        print("  closing the resource (runs even though it raised)")


try:
    run_uncaught()
except RuntimeError as error:
    print("caught outside:", error)

# try/except/else/finally all together - the full picture.
def parse(value):
    try:
        number = int(value)
    except ValueError:
        print(f"  {value!r} is not a number")
        return None
    else:
        print(f"  parsed {value!r} -> {number}")
        return number
    finally:
        print("  done with this value")


for item in ["42", "abc"]:
    parse(item)

# The `with` statement is the idiomatic "always clean up" pattern for files.
import os, tempfile
path = os.path.join(tempfile.gettempdir(), "finally_demo.txt")
try:
    with open(path, "w") as handle:
        handle.write("data")
    print("file written and closed automatically")
finally:
    if os.path.exists(path):
        os.remove(path)
        print("temporary file removed")
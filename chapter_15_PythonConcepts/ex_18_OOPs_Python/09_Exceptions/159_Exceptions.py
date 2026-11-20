# 159_Exceptions.py
# Demonstrates a NameError: 'a' is used before it is defined, so Python stops
# with "name 'a' is not defined".
# The unhandled version, kept in a try so the rest of the file still runs:
try:
    print(a)
except NameError as error:
    print("NameError:", error)
# NameError: name 'a' is not defined

# More complex: handle the NameError and see the difference between an
# undefined name and a name that exists but holds a falsy value.
try:
    print(undefined_variable)
except NameError as error:
    print("NameError:", error)

# Python also raises NameError for a misspelled builtin or a local used before
# assignment inside a function.
def local_scope():
    try:
        print(value)          # local not assigned yet
    except (NameError, UnboundLocalError) as error:
        print("caught inside function:", type(error).__name__)
    value = 10                # assignment makes `value` local for the whole function
    print("value after assignment:", value)


local_scope()

# Checking a name safely without triggering NameError:
safe_name = "a" in globals() or "a" in locals()
print("is 'a' defined here?", safe_name)

# The exception object carries a useful message.
try:
    a
except NameError as error:
    print("message:", error, "| args:", error.args)
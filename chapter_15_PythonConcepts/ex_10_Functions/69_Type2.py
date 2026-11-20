# 69_Type2.py
# Function type 2: takes no parameters but returns a value, which is stored
# in a variable and then printed.
def greet():
    return "Hi"


msg = greet()
print(msg)

# More complex: a no-parameter function that returns a fresh value each call
# (inside, it uses mutable state that persists between calls).
import itertools

_counter = itertools.count(1)


def next_test_id():
    return f"TC-{next(_counter):03d}"


print(next_test_id())
print(next_test_id())

# Returning a container instead of a single value is also type 2 in spirit.
def default_config():
    return {"timeout": 30, "retries": 3}


print(default_config())
print(type(default_config()))
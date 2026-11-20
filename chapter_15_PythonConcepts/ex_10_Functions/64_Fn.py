# 64_Fn.py
# First function example: defines a simple greet() function with def and
# calls it once to print "Hello".
# Def

def greet():
    print("Hello")
# Call
greet()

# More complex: a function that takes a name and a greeting, returns a string,
# and is reused for several values.
def greet_person(name, greeting="Hello"):
    return f"{greeting}, {name}!"


print(greet_person("Pramod"))
print(greet_person("Amit", "Welcome"))

# Functions can take other functions as arguments.
def apply_twice(fn, value):
    return fn(fn(value))


print(apply_twice(lambda n: n + 3, 10))

# A docstring documents the function, and __doc__ reads it back.
def square(n):
    """Return n multiplied by itself."""
    return n * n


print(square(7), "|", square.__doc__)

# Calling a function before defining it raises NameError, so order matters
# at module level (unlike inside another function).
print("name:", greet.__name__)

# util_normal.py
# Empty placeholder module inside a plain (non-package) folder. It has no code;
# it exists to contrast a normal directory with a real Python package.

# More complex: even a plain module without __init__.py can hold reusable
# functions - it just is not part of an importable package structure.
def normal_greet(name):
    return f"Hello from util_normal, {name}"


def normal_sum(*numbers):
    return sum(numbers)


if __name__ == "__main__":
    print(normal_greet("Pramod"))
    print(normal_sum(1, 2, 3))

# Notice the difference: util_normal.py is a lone module, while the sibling
# "package/" folder has __init__.py and can be imported as "package".

# 49_Multiple.py
# Structural pattern matching on a tuple: matches the origin, points on the
# X/Y axis (capturing the non-zero value), or an arbitrary (x, y) point.
point = (10, 20)

match point:
    case (0, 0):
        print("Origin")
    case (0, y):
        print("Y-axis:", y)
    case (x, 0):
        print("X-axis:", x)
    case (x, y):
        print("Point:", x, y)

# Here, x and y capture values from the tuple.

# More complex: match on lists, dicts and class instances with patterns.
def describe(data):
    match data:
        case []:
            return "empty list"
        case [x]:
            return f"list with one item: {x}"
        case [x, y]:
            return f"pair: {x} and {y}"
        case [first, *rest]:
            return f"first={first}, rest={rest}"
        case {"type": "user", "name": name}:
            return f"user named {name}"
        case {"type": kind}:
            return f"unknown record of type {kind}"
        case _:
            return "something else"


for item in [[], [1], [1, 2], [1, 2, 3, 4],
             {"type": "user", "name": "pramod"},
             {"type": "order"}, "text"]:
    print(f"{str(item):<38} -> {describe(item)}")
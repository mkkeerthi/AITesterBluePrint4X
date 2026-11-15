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
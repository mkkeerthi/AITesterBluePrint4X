# 98_Tuple.py
# Shows that tuples are immutable: assigning to my_tuple[0] raises a TypeError
# ("'tuple' object does not support item assignment").
my_tuple = (1, 2, 3)
print(my_tuple)
# Wrapped in try/except so the rest of the file can still run.
try:
    my_tuple[0] = 12
except TypeError as error:
    print("TypeError:", error)
print(my_tuple)

# More complex: the immutability rules practically - what you CAN do with a
# tuple (read, slice, concatenate, unpack) and how to change one properly.
coords = (10, 20, 30)
print("First:", coords[0], "Last:", coords[-1])
print("Slice:", coords[1:])
print("Concatenated:", coords + (40, 50))
print("Repeated:", (0, 1) * 3)
print("Length:", len(coords), "Contains 20:", 20 in coords)

# To "modify" a tuple, build a new one (or convert to list and back).
updated = list(coords)
updated[0] = 99
updated = tuple(updated)
print("updated tuple:", updated)

# Unpacking, and the two-element swap that works thanks to tuples.
x, y, z = coords
print(x, y, z)
a, b = 1, 2
a, b = b, a
print("swapped:", a, b)

# A tuple can safely be a dict key or a set member because it is hashable.
locations = {("delhi", 110001): "HQ", ("mumbai", 400001): "Branch"}
print(locations[("delhi", 110001)])
print({(1, 2), (3, 4)})

# Errors when trying in-place methods a list has:
try:
    coords.append(40)
except AttributeError as error:
    print("AttributeError:", error)

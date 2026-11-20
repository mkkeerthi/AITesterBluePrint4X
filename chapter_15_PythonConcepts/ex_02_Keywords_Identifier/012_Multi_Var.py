# 012_Multi_Var.py
# Multiple assignment (tuple unpacking): three variables are assigned three
# values of different types in a single line.
a, b, c = 45, 5.4, "pramod"
print(a)
print(b)
print(c)

# More complex: swap without a temp variable, unpack a list, and use * to
# collect the "rest" into a list.
x, y = 10, 20
x, y = y, x
print("Swapped:", x, y)

coordinates = [10.5, 20.7, 30.1]
lat, lon, altitude = coordinates
print(lat, lon, altitude)

first, *middle, last = [1, 2, 3, 4, 5]
print("First:", first)
print("Middle:", middle)
print("Last:", last)

# Same idea with strings: unpack the first two characters.
head, *tail = "PYTHON"
print(head, tail)
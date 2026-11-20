# 89_TypeConversion.py
# Shows explicit type conversion: the string "10" is converted to an int with
# int(), and the available converter functions are listed in a comment.
a = "10"
print(type(a))
a = int(a)
print(type(a))

# int(), str(), float(),
# bool(), list(), tuple(),set(), dict(),
# complex()

# More complex: each converter applied to the same inputs, and the ways a
# conversion can fail.
samples = ["10", "3.14", "True", "hello", "1,2,3"]

for value in samples:
    conversions = {}
    for name, fn in [("int", int), ("float", float), ("bool", bool)]:
        try:
            conversions[name] = fn(value)
        except ValueError:
            conversions[name] = "error"
    print(f"{value!r:<10} -> {conversions}")

# Explicit vs implicit conversion: Python will not auto-convert str to int.
print(int("10") + 5)          # explicit
print(str(10) + "5")          # explicit, gives "105"

# Container conversions.
print(list("abc"), tuple([1, 2]), set([1, 2, 2, 3]), dict([("a", 1)]))
print(int(3.99), float(3), bool([]), complex(2))

# None cannot be converted to a number - that raises TypeError.
try:
    int(None)
except TypeError as error:
    print("TypeError:", error)
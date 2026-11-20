# 163_IndexError.py
# Demonstrates an IndexError: index 4 does not exist in a 3-item list.
my_list = [1, 2, 3]
try:
    print(my_list[4])
except IndexError as error:
    print("IndexError:", error)
# IndexError: list index out of range

# More complex: catch the IndexError and use the safe access patterns that
# avoid it entirely (guard the length, or use try/except with a default).
try:
    print(my_list[4])
except IndexError as error:
    print("caught:", error)

def get_item(items, index, default=None):
    try:
        return items[index]
    except IndexError:
        return default


for index in [0, 2, 4, -1, -10]:
    print(f"[{index}] -> {get_item(my_list, index, 'out of range')}")

# Guarding with len() works, but negative indexes need care.
index = 3
if 0 <= index < len(my_list):
    print(my_list[index])
else:
    print("index out of range")

# Slicing never raises for out-of-range indexes - it just returns less data.
print("slice:", my_list[1:100])

# KeyError is the dictionary equivalent of IndexError.
try:
    {"a": 1}["b"]
except KeyError as error:
    print("KeyError:", error)
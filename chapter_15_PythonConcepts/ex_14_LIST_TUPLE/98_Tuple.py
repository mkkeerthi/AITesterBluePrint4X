# 98_Tuple.py
# Shows that tuples are immutable: assigning to my_tuple[0] raises a TypeError
# ("'tuple' object does not support item assignment").
my_tuple = (1, 2, 3)
print(my_tuple)
my_tuple[0] = 12
print(my_tuple)

# 101_Tuple.py
# Converts a tuple into a list with list(), which makes it mutable if needed;
# the immutable tuple of API URLs is printed alongside its list version.
shopping_list_wife = ["bread", "butter", "paneer"]


my_tuple = ("tta.com", "sdet.live")
print(my_tuple)
my_api_list = list(my_tuple)
print(my_api_list)

# More complex: the round trip tuple -> list -> tuple, and why a shallow
# conversion does not protect nested mutable objects.
my_api_list.append("awesomeqa.com")
my_api_list[0] = "thetestingacademy.com"
print("modified list:", my_api_list)

back_to_tuple = tuple(my_api_list)
print("back to tuple:", back_to_tuple)

# Shallow vs deep: nested lists inside a tuple are still mutable.
config = ("prod", ["api", "web"])
config[1].append("worker")     # allowed - the inner list is mutable
print("nested change:", config)

try:
    config[1] = []
except TypeError as error:
    print("but the tuple slot is fixed:", error)

# copy.deepcopy gives a fully independent structure when needed.
import copy
deep = copy.deepcopy(config)
deep[1].append("cron")
print("original:", config)
print("deep copy:", deep)

# Tuples of tuples are the fully immutable option.
frozen = ("prod", ("api", "web"))
print("fully immutable:", frozen)
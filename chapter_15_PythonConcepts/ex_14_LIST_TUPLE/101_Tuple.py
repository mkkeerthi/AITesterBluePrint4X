# 101_Tuple.py
# Converts a tuple into a list with list(), which makes it mutable if needed;
# the immutable tuple of API URLs is printed alongside its list version.
shopping_list_wife = ["bread", "butter", "paneer"]


my_tuple = ("tta.com", "sdet.live")
print(my_tuple)
my_api_list = list(my_tuple)
print(my_api_list)
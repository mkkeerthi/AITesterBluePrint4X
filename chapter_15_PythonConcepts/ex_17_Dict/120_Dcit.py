# 120_Dcit.py
# Builds a dictionary by pairing two lists with dict(zip(keys, values)) - extra
# values are ignored - then shows that dict equality does not depend on key order.
keys = ["name", "role", "experience", "abc"]
values = ["Aman", "SDET", 3, 67,90]
# values = ["Aman", "SDET"]

my_dict = dict(zip(keys, values))
print(my_dict)

dict1 = {"a": 1, "b": 2}
dict2 = {"b": 2, "a": 1}

print(dict1 == dict2)
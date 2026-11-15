# 116_Dict.py
# Dictionary basics: create key-value pairs, read values by key, update a value,
# delete a key with del, loop over items(), and test key membership with "in".
my_dict = {
    "name": "Aman",
    "age": 34,
    "role": "SDET",
    "exp": 3
}

print(my_dict)
print(my_dict["age"])
print(my_dict["role"])

my_dict["role"] = "Manual Tester"
print(my_dict)

del my_dict["age"]
print(my_dict)


for key, value in my_dict.items():
    print(key, value)

print("age" in my_dict)
print("role" in my_dict)
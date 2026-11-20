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

# More complex: safe access with get(), required-key checks, and building a
# dictionary from scratch while looping.
profile = {"name": "Aman", "role": "SDET"}

print(profile.get("role"))
print(profile.get("email"))                    # None, no KeyError
print(profile.get("email", "not provided"))    # default value

# Indexing a missing key DOES raise KeyError, so get() is safer for optional data.
try:
    profile["email"]
except KeyError as error:
    print("KeyError:", error)

# Build a frequency table - the most common dictionary pattern.
words = "to be or not to be".split()
freq = {}
for word in words:
    freq[word] = freq.get(word, 0) + 1
print(freq)

# The same with a defaultdict (no get() needed).
from collections import defaultdict

freq2 = defaultdict(int)
for word in words:
    freq2[word] += 1
print(dict(freq2))

# Update several keys at once, then inspect keys/values/items as views.
profile.update({"role": "Senior SDET", "exp": 5})
print(list(profile.keys()), list(profile.values()), len(profile))
# 102_Example.py
# Tuple examples: len() gives the item count, "in" checks membership, tuple()
# builds a tuple from a list of API URLs, and a for loop iterates the tuple.
cities = ("London", "Paris", "Los Angeles", "Tokyo")
print(len(cities))

print("Paris" in cities)
print("New Delhi" in cities)


ENV_API_URLS = tuple(["abc.com/get", "xyz.com/post", "qwe.com/put"])
print(ENV_API_URLS)



colors = ("red", "green", "blue")
for c in colors:
    print(c)
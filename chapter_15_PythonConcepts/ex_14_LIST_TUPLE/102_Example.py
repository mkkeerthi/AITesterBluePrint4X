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

# More complex: tuple tricks used in real code - enumerate, zip, and
# returning several values, plus a search that reports the position.
for position, colour in enumerate(colors, start=1):
    print(f"{position}. {colour}")

pairs = list(zip(colors, ["#f00", "#0f0", "#00f"]))
print("pairs:", pairs)

def min_max(values):
    return min(values), max(values)   # a tuple is returned

low, high = min_max([3, 9, 1, 7])
print("low/high:", low, high)

# Membership plus index, without raising on a miss.
city = "Berlin"
if city in cities:
    print(f"{city} is at index {cities.index(city)}")
else:
    print(f"{city} is not in the tuple (default -> 0)")

# Counting and joining, and an attempt at an in-place sort kept as an error.
print("cities:", len(cities), "|", ", ".join(cities))
try:
    cities.sort()
except AttributeError as error:
    print("tuples have no sort():", error)
print("sorted copy:", tuple(sorted(cities)))
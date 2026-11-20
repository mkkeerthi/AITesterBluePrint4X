# 100_LIST_TUPle.py
# Practical use of tuples: a fixed set of API base URLs that should not change,
# highlighted by comparing it with a mutable shopping list, plus tuple()/list() constructors.
# Real case, where we Tuples
API_URLSs = ("https://sdet.live/python0x", "https://awesomeqa.com", "https://thetestingacademy.com")
print(API_URLSs[0])
print(API_URLSs[1])

# Real of Tuples
my_tuple = ("tta.com", "sdet.live")
print(my_tuple)
my_api_list = list(my_tuple)


shopping_list_wife = ["bread", "butter", "paneer"]
shopping_list_wife[2] = "milk"
print(shopping_list_wife)


t = tuple()
print(t)

l = list()
print(l)

# More complex: use tuples for fixed data and lists for data that changes,
# and build a lookup from a tuple of (name, url) pairs.
ENDPOINTS = (
    ("python", "https://sdet.live/python0x"),
    ("awesome", "https://awesomeqa.com"),
    ("tta", "https://thetestingacademy.com"),
)

lookup = dict(ENDPOINTS)
print(lookup["awesome"])

for name, url in ENDPOINTS:
    print(f"{name:<8} -> {url}")

# Tuples are safe to share; the "constant" cannot be reassigned by accident.
try:
    ENDPOINTS[0] = ("hacked", "x")
except TypeError as error:
    print("Tuple is immutable:", error)

# The shopping list, by contrast, changes freely and records a history.
shopping = ["bread", "butter", "paneer"]
history = []
history.append(tuple(shopping))   # snapshot the state
shopping[2] = "milk"
history.append(tuple(shopping))
print("history:", history)

# Sets of tuples remove duplicates, something lists cannot do.
visits = [("delhi", 1), ("delhi", 1), ("mumbai", 2)]
print("unique visits:", set(visits))
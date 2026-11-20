# 111_IQ.py
# Uses map() with a named function to convert every name in a list to uppercase.
name = ["pramod", "dutta", "qa", "lucky"]

def upper_case(string):
    return string.upper()


upper_name_list = list(map(upper_case, name))
print(upper_name_list)

# More complex: chaining map with other operations, and handling uneven
# lengths with a sentinel value using zip_longest.
print("titled:", list(map(str.title, name)))
print("lengths:", list(map(len, name)))

from itertools import zip_longest

first = ["pramod", "amit"]
last = ["dutta"]
combined = list(map(
    lambda pair: f"{pair[0]} {pair[1]}",
    zip_longest(first, last, fillvalue=""),
))
print("combined:", combined)

# Mapping over a dict: by default iterating a dict yields its keys.
scores = {"pramod": 91, "amit": 47}
print("keys upper:", list(map(str.upper, scores)))
print("values doubled:", list(map(lambda v: v * 2, scores.values())))

# Realistic: normalise a list of test names for reporting.
raw_names = [" login page ", "checkout_flow", " User Profile "]
report_names = list(map(lambda n: n.strip().replace("_", " ").title(), raw_names))
print(report_names)
# 115_REAL_IQ.py
# Uses filter() to remove empty strings from a list, keeping only real values;
# the predicate returns True for non-empty strings and None (falsy) otherwise.
names = ["QA", "", "Automation", "", "Tester"]

def non_empty(x):
    if x != "":
        return True
    return None


non_empty = list(filter(non_empty, names))  # removes empty strings
print(non_empty)

# More complex: filter() with None is the shorthand for "keep truthy values",
# and a realistic cleaning pipeline built from filter + map.
messy = ["QA", "", None, "  ", "Automation", 0, "Tester", False]
cleaned = list(filter(None, messy))
print("truthy:", cleaned)

# Strip each string and drop the ones that become empty.
pipeline = list(filter(None, map(lambda s: s.strip() if isinstance(s, str) else s, messy)))
print("cleaned:", pipeline)

# Clean a list of user records: only complete ones survive.
users = [
    {"name": "Pramod", "email": "p@x.com"},
    {"name": "", "email": "empty@x.com"},
    {"name": "Amit", "email": ""},
]
complete = list(filter(lambda u: u["name"] and u["email"], users))
print("complete users:", complete)

# Count the dropped records for reporting.
print(f"kept {len(complete)} of {len(users)}")
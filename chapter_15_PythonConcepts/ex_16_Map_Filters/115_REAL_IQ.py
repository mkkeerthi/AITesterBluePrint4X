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
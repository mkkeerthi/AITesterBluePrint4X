# 004_Keywords.py
# Shows that one variable can hold different data types (int, float, string)
# and prints the full list of Python reserved keywords using keyword.kwlist.
a = 10
a = 4.5
a = "pramod"

# print()
# class
# None
# break

import keyword
print(keyword.kwlist)

# More complex: check whether a name is a keyword before using it.
candidate_names = ["age", "class", "total_marks", "for", "if", "_value"]

for name in candidate_names:
    if keyword.iskeyword(name):
        print(f"'{name}' is a reserved keyword - cannot be used as a variable")
    else:
        print(f"'{name}' is a valid variable name")

# Soft keywords are special only in certain places (match, case, type, _).
print("Soft keywords:", keyword.softkwlist)
# 25_IQ.py
# Builds a full name by concatenating two strings with a space in between
# using the + operator, then prints its type.
first_name = "Pramod"
last_name = "Dutta"
full_name = first_name + " " + last_name
print(full_name)
print(type(full_name))

# More complex: the same job with f-strings and join(), which scale better.
print(f"{first_name} {last_name}")
print(" ".join([first_name, last_name]))

# Building a report line from several pieces, with formatting.
score = 87.456
print(f"{full_name} scored {score:.1f}% and {10 - 3} tests remained")

# Adding strings in a loop is inefficient; join() collects them in one pass.
lines = []
for test in ["login", "search", "checkout"]:
    lines.append(f"test_{test}")
print(" | ".join(lines))
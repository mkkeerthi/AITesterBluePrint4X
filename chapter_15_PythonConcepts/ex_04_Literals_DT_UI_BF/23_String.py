# 23_String.py
# Explains strings: both single and double quotes create a str, and shows
# common string operations len(), upper() and lower().
# Strings
name = "Pramod"
c = "C"
c1 = 'C'
print(type(c))
print(type(c1))

# <class 'str'>
# <class 'str'>

print(len(name))
print(name.upper())
print(name.lower())

# More complex: the most useful string methods and slicing.
text = "  API Test Automation  "
print(text.strip())              # remove surrounding spaces
print(text.strip().replace("Test", "UI"))
print(text.strip().split(" "))   # split into words
print("-".join(["GET", "users", "1"]))
print(text.strip().startswith("API"))
print(text.strip().endswith("Automation"))
print(name[:3], name[-3:])       # slicing: first 3, last 3
print(name[::-1])                # reverse
print("pramod" in name.lower())  # membership (case-insensitive)

# Strings are immutable: methods return new strings.
original = "hello"
changed = original.upper()
print(original, changed)
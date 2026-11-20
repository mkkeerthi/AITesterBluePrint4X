# 65_Fn.py
# Introductory notes on functions: reusable blocks of code, split into built-in
# (provided by Python) and user-defined/custom functions. No function is defined here.
# Functions - reusable block of code. 
# Built in - Python guys
# User Defined / Custom

print("Hello World")
name= input("Enter the name")

# More complex: a custom function next to a built-in one. Define it once,
# then reuse it for several inputs.
def build_greeting(name, greeting="Hello"):
    return f"{greeting}, {name}!"


people = ["Pramod", "Amit", "Navita"]
for person in people:
    # built-in len(), custom build_greeting()
    print(build_greeting(person), f"(name length {len(person)})")

print(build_greeting("Pramod", greeting="Welcome"))
# 75_UI.Fn.py
# Combines user input with a function: reads a name with input() and passes
# it to say_your_name() to print a greeting.
user_input = input("Enter your name\n")

def say_your_name(name):
    print("Hi,", name)


say_your_name(user_input)

# More complex: read, validate and convert input, then pass it to a function.
# The input() call is replaced with a fixed value so the file runs unattended.
raw_name = "Pramod"
raw_age = "30"

def build_profile(name, age):
    name = name.strip().title()   # normalise the text
    if not name:
        return "Anonymous", None
    try:
        age_value = int(age)
    except ValueError:
        return name, "unknown"
    return name, age_value


print(build_profile(raw_name, raw_age))
print(build_profile("   ", raw_age))
print(build_profile(raw_name, "not-a-number"))
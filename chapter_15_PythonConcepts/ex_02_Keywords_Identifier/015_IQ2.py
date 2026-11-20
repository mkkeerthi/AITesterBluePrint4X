# 015_IQ2.py
# Shows how to fix a TypeError: the integer is converted to a string with str()
# before concatenating it to "Hello".
# print("Hello" + 15)
print("Hello" + str(15))

# More complex: the other explicit conversions and what they do.
print(int("42") + 8)        # string -> int
print(float("3.14") * 2)    # string -> float
print(bool(""), bool("x"))  # empty string is False, non-empty is True
print(list("abc"))          # string -> list of characters

# A realistic task: read numeric input safely, convert, then calculate.
# (input() is commented out so the file runs unattended.)
# age = int(input("Enter your age: "))
age = "35".strip()          # pretend the user typed "35"
age_as_int = int(age)
print(f"Next year you will be {age_as_int + 1}")

# int() on a bad value raises ValueError, so guard the conversion.
raw = "abc"
try:
    print(int(raw))
except ValueError:
    print(f"'{raw}' is not a number - could not convert")
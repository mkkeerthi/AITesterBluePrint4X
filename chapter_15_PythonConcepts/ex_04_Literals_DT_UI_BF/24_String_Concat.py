# 24_String_Concat.py
# Demonstrates type conversion: the string "90" is converted to an integer
# with int(), printing the type before and after.
age = "90"
print(type(age))

age = int(age)
print(type(age))

# More complex: round-trip conversions and the failure cases.
number_text = "1250"
number = int(number_text)
print(number + 50)
print(str(number) + " is now text again")

price = float("19.99")
print(round(price * 3, 2))

# A bad conversion raises ValueError, so wrap it in try/except.
for raw in ["15", "3.5", "abc", ""]:
    try:
        print(f"{raw!r:<6} -> {int(raw)}")
    except ValueError as error:
        print(f"{raw!r:<6} -> ValueError: {error}")

# int() truncates floats towards zero; use round() if you want rounding.
print(int(3.99), round(3.99))
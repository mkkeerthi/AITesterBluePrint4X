# 36.py
# Simple equality comparison: proves 2 == 2 is True and 2 == 3 is False.
#  ==  Compare Operator ( True or False )
print(2 == 2)
print(2 == 3)

# More complex: comparing strings, floats and mixed types.
print("2" == 2)          # False - different types, no conversion
print(2 == 2.0)          # True - numeric value is equal
print("pramod" == "Pramod")  # False - case sensitive
print("pramod".lower() == "PRAMOD".lower())  # True

# Comparing a computed value against an expected one (the core of a test).
actual_total = 5 * 4
expected_total = 40 // 2
print(actual_total == expected_total)

# == never raises for mismatched types; it just returns False.
print([1, 2] == (1, 2))
print(None == 0)
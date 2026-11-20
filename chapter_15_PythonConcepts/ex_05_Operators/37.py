# 37.py
# Applies not to a boolean and shows relational comparisons (>, <, >=) and
# equality between two numbers, including that a >= b is true when a == b.
is_pramod_married = True
print(not is_pramod_married)
print(is_pramod_married)

# Logical Operator -> bool
# > , <  >= <=
x = 10
y = 20
print(x > y)
print(x < y)

print(" --- ")

a = 10
b = 10
print(a == b)
print(a >= b) # 10 > 10 or 10 = 10

# More complex: combine comparison results with logical operators.
age = 25
has_id = True
can_enter = age >= 18 and has_id
print(can_enter)

# Comparing a value against a valid range, written both ways.
score = 72
in_range = 0 <= score <= 100
print(in_range)

# Using comparisons in a ternary to produce a label.
grade = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "F"
print(grade)

# not with a comparison flips the answer.
print(not (a != b), not is_pramod_married)
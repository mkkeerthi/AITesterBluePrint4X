# 71_Type4.py
# Function type 4: takes parameters and returns a result (a + b), which the
# caller stores and prints.
def sum_of_two(a, b):
    return a+b

result = sum_of_two(4, 5)
print(result)

# More complex: arguments + return with validation, and a function whose
# return value feeds straight into another expression.
def safe_divide(a, b):
    if b == 0:
        return None
    return a / b


print(safe_divide(10, 2))
print(safe_divide(10, 0))

# The return value can be used inline: chained, added, or in a format string.
print(safe_divide(sum_of_two(4, 5), 3))
print(f"Half of 9 is {sum_of_two(4, 5) / 2}")

# Returning different types depending on the branch is allowed but worth noting.
def classify(n):
    if n < 0:
        return "negative"
    return n


print(classify(-1), classify(5))
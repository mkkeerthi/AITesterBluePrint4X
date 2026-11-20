# 010_IQ_Math.py
# Basic arithmetic with variables: adds two numbers, then reuses the result
# to subtract 10 and prints the value at each step.
a = 10
b = 10
c = a + b
print(c)
c = c - 10
print(c)

# More complex: a running total with compound assignment operators.
cart = [120, 250, 99, 349]
total = 0

for price in cart:
    total += price  # same as total = total + price
print("Total:", total)

discount = 0.10
total -= total * discount  # apply 10% off
print("After discount:", total)

total *= 2  # double the order
print("Doubled:", total)

# The same thing as one expression, using built-in functions.
print("Sum:", sum(cart))
print("Average:", sum(cart) / len(cart))
print("Max:", max(cart), "Min:", min(cart))
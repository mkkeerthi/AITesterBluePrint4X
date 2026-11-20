# 31_Arth_Op.py
# Covers assignment and arithmetic operators. Most examples are commented out;
# the live part shows unary + / - and incrementing a counter variable by 1.
# a = 10;
# # Assignment Operator - Assign the value of the right-hand side to the left-hand side. 

# # Arthematic

# # +, - , * , /
# print(2+2)
# print(2-2)
# print(2/2) # float
# print(2*2)


# a, b = 10, 3
# print(a + b)  # 13
# print(a - b)  # 7
# print(a * b)  # 30
# print(a / b)  # 3.3333
# print(a // b) # 3 - R
# print(a % b)  # 1 - Q
# print(a ** b) # 1000


age = +65
age2 = -65
print(age)
print(age2)

how_many_lambo_pramod = -1
how_many_lambo_pramod = how_many_lambo_pramod + 1
print(how_many_lambo_pramod)

# More complex: every arithmetic operator in one realistic calculation.
price = 1250
quantity = 3
tax_percent = 18

subtotal = price * quantity
tax = subtotal * tax_percent / 100
total = subtotal + tax

print(f"Subtotal: {subtotal}")
print(f"Tax ({tax_percent}%): {tax:.2f}")
print(f"Total: {total:.2f}")

# // and % work together: split a total into boxes of 12.
items = 100
per_box = 12
print("Full boxes:", items // per_box, "loose items:", items % per_box)

# A string can be repeated with *, and averaged with /.
print("=" * 20)
print("Average price:", subtotal / quantity)


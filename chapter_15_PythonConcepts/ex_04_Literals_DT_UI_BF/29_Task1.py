# 29_Task1.py
# Practice task (no code yet): take three inputs from the user and perform
# addition, subtraction, multiplication and division on them.
# Task for the Today
# Take a 3 input from the user
# perform the sum, sub, mul and div

# Example solution (inputs are hard-coded so the file runs unattended).
# Replace the values with int(input(...)) to read them from the user.
a, b, c = 20, 5, 2

print(f"Sum        : {a + b + c}")
print(f"Subtraction: {a - b - c}")
print(f"Multiply   : {a * b * c}")

# Guard the division against a zero denominator.
if b != 0 and c != 0:
    print(f"Division   : {a / b / c}")
    print(f"Floor div  : {a // b // c}")
    print(f"Remainder  : {a % b}")
else:
    print("Division   : skipped (cannot divide by zero)")
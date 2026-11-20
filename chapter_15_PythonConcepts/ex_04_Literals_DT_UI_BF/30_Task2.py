# 30_Task2.py
# Practice task (no code yet): take two inputs from the user and print the
# quotient and remainder of their division (15 / 2 -> Q=7, R=1).
# Task for the Today
# Take a 2 input from the user
# Print the Quotient and Remainder
# 15 ->  num1
# 2 -> num2
# Q -> 7
# R -> 1

# Example solution using divmod(), which returns both values in one call.
# Swap these for int(input(...)) to read them from the user.
num1 = 15
num2 = 2

if num2 == 0:
    print("Cannot divide by zero")
else:
    quotient, remainder = divmod(num1, num2)
    print(f"{num1} / {num2} -> Q = {quotient}, R = {remainder}")

# Generalised: same logic for a list of pairs.
for dividend, divisor in [(15, 2), (100, 7), (9, 3), (7, 0)]:
    if divisor == 0:
        print(f"{dividend} / {divisor} -> undefined")
    else:
        q, r = divmod(dividend, divisor)
        print(f"{dividend} / {divisor} -> Q = {q}, R = {r}")
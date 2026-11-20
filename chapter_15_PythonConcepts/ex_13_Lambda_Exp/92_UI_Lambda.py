# 92_UI_Lambda.py
# Uses lambdas with user input: checks even/odd via a ternary inside a lambda,
# shows an immediately-invoked lambda, and computes a square with math.pow().
user_input = int(input("Enter the number"))
check_even_odd_f = lambda num: "Even" if num % 2 == 0 else "Odd"
result = check_even_odd_f(user_input)
print(result)

# Alternate in one line
print((lambda num: "Even" if num % 2 == 0 else "Odd")(int(input("Enter the number: "))))



import math
op2 = lambda: math.pow(int(input("Enter the number")), 2)
print(op2())

# More complex: validate input, then apply several lambdas stored in a dict -
# a tiny "command table" without any if/elif chain.
raw = "12"  # replace with input("Enter a number") to read from the user

try:
    number = int(raw)
except ValueError:
    print(f"'{raw}' is not a number")
else:
    operations = {
        "double": lambda n: n * 2,
        "square": lambda n: n ** 2,
        "is_even": lambda n: n % 2 == 0,
        "sign": lambda n: "positive" if n > 0 else "negative" if n < 0 else "zero",
    }
    for label, operation in operations.items():
        print(f"{label:<8} -> {operation(number)}")

    # Lambdas inside a comprehension, applied to a whole list.
    values = [1, 2, 3, 4]
    print([(lambda v: v * 10)(v) for v in values])
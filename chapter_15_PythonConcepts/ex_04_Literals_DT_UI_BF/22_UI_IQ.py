# 22_UI_IQ.py
# Takes two numbers from the user as text, converts them to integers with
# int(), and prints their sum (without the conversion they would be concatenated).
num1 = int(input("Enter num 1 -> "))
num2 = int(input("Enter num 2 -> "))
print(num1+num2)

# More complex: handle bad input and divide safely instead of crashing.
def read_int(prompt, default):
    # input() is replaced by a default so this file runs without a keyboard.
    raw = str(default)
    try:
        return int(raw)
    except ValueError:
        print(f"'{raw}' is not an integer - using 0")
        return 0


a = read_int("Enter num 1 -> ", "18")
b = read_int("Enter num 2 -> ", "0")

print("Sum:", a + b)
if b == 0:
    print("Cannot divide by zero")
else:
    print("Division:", a / b)
    print("Quotient:", a // b, "Remainder:", a % b)
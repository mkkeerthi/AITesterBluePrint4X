# 168_Fix3.py
# Handles two possible failures separately: a non-numeric input raises
# ValueError and division by zero raises ZeroDivisionError; each has its own except block.
try:
    a = int(input("Enter num 1"))
    b = int(input("Enter num 2"))
    c = a / b
    print(c)
except ValueError:
    print("Value Error")
except ZeroDivisionError:
    print("Div Error")
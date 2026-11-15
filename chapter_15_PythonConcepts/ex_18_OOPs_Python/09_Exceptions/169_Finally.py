# 169_Finally.py
# Adds finally to the try/except: the finally block runs no matter what, whether
# an exception was raised, caught, or no error occurred at all.
try:
    a = int(input("Enter num 1"))
    b = int(input("Enter num 2"))
    c = a / b
    print(c)
except ValueError:
    print("Value Error")
except ZeroDivisionError:
    print("Div Error")
finally:
    print("I will always execute!")
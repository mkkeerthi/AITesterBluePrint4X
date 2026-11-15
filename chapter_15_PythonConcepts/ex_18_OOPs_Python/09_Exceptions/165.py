# 165.py
# The "problem" version: reads two numbers and divides them with no error
# handling, so entering 0 as the second number raises ZeroDivisionError.
a = int(input("Enter num 1"))
b = int(input("Enter num 2"))
c = a/b
print(c)
# ZeroDivisionError: division by zero
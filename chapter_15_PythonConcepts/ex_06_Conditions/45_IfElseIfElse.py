# 45_IfElseIfElse.py
# Nested if/else: reads a number and first checks whether it is non-negative,
# then uses modulo (%) to report whether it is Even or Odd, or else Negative.
# Find the positive number is even or odd

num = int(input("Enter a numner").strip())

if  num>=0:
    if num%2 ==0:
        print("Even")
    else:
        print("Odd")
else:
    print("Negative Number!")
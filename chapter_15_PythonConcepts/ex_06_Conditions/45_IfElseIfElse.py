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

# More complex: classify every number in a list using nested conditions.
def classify(value):
    if value >= 0:
        if value == 0:
            return "zero"
        return f"positive {'even' if value % 2 == 0 else 'odd'}"
    return f"negative {'even' if value % 2 == 0 else 'odd'}"


for number in [-4, -3, 0, 7, 10]:
    print(f"{number:>3} -> {classify(number)}")
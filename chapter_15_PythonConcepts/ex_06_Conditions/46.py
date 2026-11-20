# 46.py
# Problem: find the maximum of three user-entered numbers. Solved with an
# if/elif/else chain comparing each number against the other two.
# Problem  Find the Max between 3 numbers

# User inputs - num1, num2, num3 -> int
# O/p -> int or String with max number 

num1 = int(input("Enter the num1\n"))  # 5 , # 10
num2 = int(input("Enter the num2\n"))  # 3 , # 12
num3 = int(input("Enter the num3\n"))  # 2 , # 11

# result = max(num1,num2,num3)
# print(result)

if num1 >= num2 and num1>=num3:
    print(num1)
elif num2>=num3 and num2>=num1:
    print(num2)
else:
    print(num3)

# More complex: the same "max of three" solved with a reusable function,
# using built-in max() as the reference answer (inputs are hard-coded).
def max_of_three(a, b, c):
    largest = a
    if b > largest:
        largest = b
    if c > largest:
        largest = c
    return largest


cases = [(5, 3, 2), (10, 12, 11), (-1, -5, -3), (7, 7, 7)]
for a, b, c in cases:
    result = max_of_three(a, b, c)
    print(f"max({a}, {b}, {c}) = {result}  (built-in says {max(a, b, c)})")
    assert result == max(a, b, c)
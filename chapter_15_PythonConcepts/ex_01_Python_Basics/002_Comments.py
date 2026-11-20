# 002_Comments.py
# Demonstrates single-line comments with '#': commented-out code does not run.
# Then prints arithmetic results and multiple values in one print() call.
# print("Hello TheTestingAcademy")

# This is Comment
# This code will not be executed.
#
print(2 + 2)
print(2, 3, 4)
print("Hello", True, "PrrammodDutta", 12342)

# A more realistic use of comments: document what a calculation does.
# Area of a rectangle = length * breadth
length = 12
breadth = 5
area = length * breadth
print("Area:", area)

# Comments can also sit next to code to explain a tricky line.
total = sum(range(1, 11))  # sum of 1..10 using the built-in range and sum
print("Total:", total)
# print(total * 2)  <- this line stays disabled and never runs
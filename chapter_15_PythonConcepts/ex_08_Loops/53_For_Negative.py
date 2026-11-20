# 53_For_Negative.py
# Shows the default range(10) (0 to 9) printing "Hello World!" 10 times;
# examples of negative steps are included as comments.
# for i in range(1, 10,-1):
#     print(i)

# for i in range(10, 1,-1):
#     print(i)


for i in range(10): #0 to 9, step=1
    print("Hello World!")

# More complex: counting down, and stepping through a list in reverse.
for i in range(10, 0, -1):
    print(i, end=" ")
print()

# Reversing any sequence with reversed() instead of a negative range.
for letter in reversed("PYTHON"):
    print(letter, end="")
print()

# range(stop) can never count down - it needs a negative step.
print("range(10, 0) is empty:", list(range(10, 0)))
print("range(10, 0, -2):", list(range(10, 0, -2)))

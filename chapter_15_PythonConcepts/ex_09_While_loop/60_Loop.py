# 60_Loop.py
# Nested for loops: the outer loop runs 1-2 and the inner 1-3, printing
# every (i, j) combination.
for i in range(1, 3):
    for j in range(1, 4):
        print(i, j)

# More complex: print a multiplication table and a small pattern using
# nested loops, then flatten the pairs with a comprehension.
print("Multiplication table (3x3)")
for row in range(1, 4):
    for col in range(1, 4):
        print(f"{row * col:>3}", end="")
    print()

print("Pattern")
for row in range(1, 5):
    for _ in range(row):
        print("*", end="")
    print()

pairs = [(i, j) for i in range(1, 3) for j in range(1, 4)]
print("All pairs:", pairs)

# break in the inner loop only exits the inner loop.
for i in range(1, 4):
    for j in range(1, 4):
        if j == 2:
            break
        print(f"inner {i},{j}")
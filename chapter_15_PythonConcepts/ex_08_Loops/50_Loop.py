# 50_Loop.py
# for loop over range(1, 6, 2): starts at 1, stops before 6, steps by 2,
# so it prints 1, 3, 5.
# for i in range(1, 6):
#     print(i)

# range(start, end-1, step) - G


for i in range(1, 6, 2):
    print(i)

# More complex: range() variants and looping over real collections.
print("Negative step:", list(range(10, 0, -3)))
print("Reversed:", list(range(5, 0, -1)))
print("Squares:", [n * n for n in range(1, 6)])

# Iterating with the index via enumerate().
names = ["pramod", "amit", "navita"]
for position, name in enumerate(names, start=1):
    print(f"{position}. {name}")

# Pairing two lists element by element with zip().
scores = [91, 47, 88]
for name, score in zip(names, scores):
    print(f"{name:<8} -> {score}")
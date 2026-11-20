# 64_Continue.py
# Uses continue to skip even numbers, so only the odd numbers 0-9 are printed.
for number in range(10):
    if number % 2 == 0:
        continue
    else:
        print(number)

# More complex: sum only the odd numbers, and skip values that fail validation.
total = 0
for number in range(1, 15):
    if number % 2 == 0:
        continue
    if number == 11:
        continue  # deliberately skip eleven
    total += number

print("Sum of odds 1-14 (without 11):", total)

# continue inside a nested loop only affects the innermost loop.
for row in range(1, 4):
    for col in range(1, 4):
        if col == 2:
            continue
        print(f"{row},{col}", end=" ")
    print()
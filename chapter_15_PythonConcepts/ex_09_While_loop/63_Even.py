# 63_Even.py
# Prints every even number from 0 to 100 using modulo (%) to test divisibility by 2.
for i in range(101):  # 0 to 100
    if i % 2 == 0:
        print(i)

# More complex: separate even and odd numbers, and sum them, in one pass.
evens, odds = [], []
even_sum = odd_sum = 0

for i in range(1, 21):
    if i % 2 == 0:
        evens.append(i)
        even_sum += i
    else:
        odds.append(i)
        odd_sum += i

print("Evens:", evens)
print("Odds:", odds)
print("Even sum:", even_sum, "Odd sum:", odd_sum)

# The same filter expressed with a comprehension (and range steps).
print("Evens via comprehension:", [n for n in range(1, 21) if n % 2 == 0])
print("Evens via step:", list(range(0, 21, 2)))
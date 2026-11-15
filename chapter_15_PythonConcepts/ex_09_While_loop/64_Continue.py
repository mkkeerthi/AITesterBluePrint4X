# 64_Continue.py
# Uses continue to skip even numbers, so only the odd numbers 0-9 are printed.
for number in range(10):
    if number % 2 == 0:
        continue
    else:
        print(number)
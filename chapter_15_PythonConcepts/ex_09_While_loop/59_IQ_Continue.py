# 59_IQ_Continue.py
# Demonstrates continue: when i is 3 the rest of the iteration is skipped,
# so 3 is not printed (1, 2, 4, 5 are).
for i in range(1, 6):
    if i == 3:
        continue
    print(i)
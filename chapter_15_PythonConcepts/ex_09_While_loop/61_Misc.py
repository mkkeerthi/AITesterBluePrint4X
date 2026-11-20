# 61_Misc.py
# for/else: the else block runs only if the loop finishes without hitting a
# break. Since 5 is never found, it prints "5 not found".
for number in [2,4,6]:
    if number ==5:
        break
else:
    print("5 not found")

# More complex: search a list and use for/else to report both outcomes.
target = 4

for number in [2, 4, 6]:
    if number == target:
        print(f"{target} found")
        break
else:
    print(f"{target} not found")

# The same pattern to prove every score is a pass.
scores = [90, 85, 77]
for score in scores:
    if score < 50:
        print("There is a failing score")
        break
else:
    print("All scores pass")

# try/except has an else too: it runs when no exception was raised.
try:
    value = int("42")
except ValueError:
    print("conversion failed")
else:
    print("conversion worked:", value)
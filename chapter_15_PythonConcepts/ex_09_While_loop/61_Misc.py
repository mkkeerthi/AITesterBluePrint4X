# 61_Misc.py
# for/else: the else block runs only if the loop finishes without hitting a
# break. Since 5 is never found, it prints "5 not found".
for number in [2,4,6]:
    if number ==5:
        break
else:
    print("5 not found")
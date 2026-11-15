# 62_Pass.py
# Shows pass (a no-op placeholder): prints only 5 and 6, doing nothing for
# every other number.
for i in range(0, 10, 1):
    if i == 6 or i == 5:
        print(i)
    else:
        pass # do nothing
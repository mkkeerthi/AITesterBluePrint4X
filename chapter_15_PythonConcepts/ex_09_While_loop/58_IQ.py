# 58_IQ.py
# Demonstrates break: the loop exits immediately when i reaches 3,
# so it prints only 1 and 2.
for i in range(1, 6):
    if i == 3:
        break
    print(i)

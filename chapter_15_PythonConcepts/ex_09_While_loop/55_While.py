# 55_While.py
# Basic while loop: prints the counter while count < 5 and increments it
# each iteration so the loop eventually stops.
count = 0
while count<5:
    print("Count is ",count)
    count = count+1

# More complex: a while loop that adds up numbers until a target is reached.
total = 0
number = 1
while total < 20:
    total += number
    print(f"added {number}, total is now {total}")
    number += 1
print("Stopped at total", total)

# A countdown loop (the condition drives it downward).
liftoff = 3
while liftoff > 0:
    print(f"T-minus {liftoff}")
    liftoff -= 1
print("Liftoff!")



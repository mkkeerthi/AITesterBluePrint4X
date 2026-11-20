# 40.py
# Notes that Python has no ++ / -- operators; instead it uses augmented
# assignment (+=, -=, *=) to update a variable in place.
# Increment (++) / Decrement (--) Operators
# Good news - Doesn't have ++, -- operator

x = 5
x += 1
print(x)

x -= 1  # x= x-1
print(x)

x *= 3  # x= x*1
print(x)

# More complex: all the augmented assignment operators in one place.
# +=  -=  *=  /=  //=  %=  **=  and  &= |= ^= >>= <<= for bitwise
value = 10
value += 5;   print("+=", value)     # 15
value -= 3;   print("-=", value)     # 12
value *= 2;   print("*=", value)     # 24
value /= 4;   print("/=", value)     # 6.0
value //= 2;  print("//=", value)    # 3.0
value %= 2;   print("%=", value)     # 1.0
value **= 3;  print("**=", value)    # 1.0

# A realistic counter pattern: accumulate a total and a count in a loop.
total, count = 0, 0
for price in [120, 80, 45]:
    total += price
    count += 1
print(f"{count} items, total {total}, average {total / count:.2f}")

# Note: x++ raises a SyntaxError in Python - use x += 1 instead.
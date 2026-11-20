# 013_MathIQ.py
# Prints several string arguments, concatenates two strings, then tries
# "string" + int + int, which raises a TypeError because str and int cannot be added.
print("Amit", "Teja", "Tushar")

print("PRAMOD" + "DUTTA")

# Detonation between the string and integer is not allowed in 
try:
    print("PRAMOD" + 10 + 20)
except TypeError as error:
    print("TypeError:", error)

# More complex: the fixes for that TypeError, plus what each one produces.
# 1) Convert the numbers to strings (concatenation)
print("PRAMOD " + str(10) + " " + str(20))

# 2) Let print() handle the mixed types with commas
print("PRAMOD", 10, 20)

# 3) Add the numbers first, then embed the total in text
print("PRAMOD " + str(10 + 20))

# 4) f-strings convert automatically - the cleanest option
score = 10
bonus = 20
print(f"PRAMOD scored {score + bonus} points")

# A checklist of the TypeError cases worth remembering
# "2" + 2        -> TypeError
# "2" * 2        -> "22" (string repetition, allowed)
# int("2") + 2   -> 4 (explicit conversion)
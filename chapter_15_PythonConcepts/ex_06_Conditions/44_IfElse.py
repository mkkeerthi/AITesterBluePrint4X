# 44_IfElse.py
# Basic if/else: reads the user's age and prints whether they are allowed in
# the club (age >= 21) or not.
age = int(input("Enter your age"))

if age >=21: 
    print("You can go to the club!")
else:
    print("Not Allowed!")

# More complex: elif chain with input validation (value hard-coded so the
# example runs unattended - swap in int(input(...)) to read it from the user).
def age_category(age):
    if age < 0:
        return "invalid age"
    elif age < 13:
        return "child"
    elif age < 20:
        return "teenager"
    elif age < 60:
        return "adult"
    else:
        return "senior"


for sample_age in [-1, 8, 15, 21, 45, 70]:
    print(f"{sample_age:<3} -> {age_category(sample_age)}")

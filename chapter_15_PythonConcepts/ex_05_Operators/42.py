# 42.py
# Reads the user's age and uses if/else to decide whether they may vote/travel;
# a one-line ternary alternative is included as a comment.
user_age = int(input("Enter your age\n"))

if user_age >= 18:
    print("Yes You can go to GOA and vote")
else:
    print("Not you can't go and can't vote")

# print("Yes You can go to GOA and vote" if user_age >= 18 else "Not you can't go and can't vote")

# More complex: multi-condition eligibility with elif, plus a guard for
# invalid input (input() replaced with a fixed value to run unattended).
user_age = 16

if user_age < 0 or user_age > 120:
    print("Invalid age")
elif user_age >= 18:
    print("Eligible to vote and travel")
elif user_age >= 16:
    print("Eligible to travel with guardian, not to vote")
else:
    print("Not eligible")

# The same logic as a single expression, in a function.
def eligibility(age):
    if not 0 <= age <= 120:
        return "invalid"
    return "adult" if age >= 18 else "minor"


for age in [-5, 12, 17, 18, 65, 130]:
    print(f"age {age:<4} -> {eligibility(age)}")
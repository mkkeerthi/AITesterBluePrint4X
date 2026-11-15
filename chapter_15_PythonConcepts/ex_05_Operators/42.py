# 42.py
# Reads the user's age and uses if/else to decide whether they may vote/travel;
# a one-line ternary alternative is included as a comment.
user_age = int(input("Enter your age\n"))

if user_age >= 18:
    print("Yes You can go to GOA and vote")
else:
    print("Not you can't go and can't vote")

# print("Yes You can go to GOA and vote" if user_age >= 18 else "Not you can't go and can't vote")
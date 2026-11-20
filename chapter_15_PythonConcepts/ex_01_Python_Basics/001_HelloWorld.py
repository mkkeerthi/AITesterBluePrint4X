# 001_HelloWorld.py
# The classic first Python program: prints a greeting string to the console
# using the built-in print() function.
print("Hello TheTestingAcademy")

# A slightly bigger version: greet several users using a loop and f-strings.
# f-strings (f"...{variable}...") embed values directly inside the text.
users = ["Pramod", "Amit", "Navita"]
for index, user in enumerate(users, start=1):
    print(f"{index}. Hello {user}, welcome to Python!")

print("Hello", "TheTestingAcademy", sep=" -- ", end="!\n")
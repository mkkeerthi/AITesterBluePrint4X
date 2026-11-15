# 75_UI.Fn.py
# Combines user input with a function: reads a name with input() and passes
# it to say_your_name() to print a greeting.
user_input = input("Enter your name\n")

def say_your_name(name):
    print("Hi,", name)


say_your_name(user_input)
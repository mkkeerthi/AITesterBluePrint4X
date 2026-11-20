# 68_Type1.py
# Function type 1 again: no parameters, no return value - defines greet() and calls it.
def greet():
    print("Hello")
# Call
greet()

# More complex: type 1 in a few new guises - same signature, different bodies.
def show_menu():
    for item in ["1. Run tests", "2. View report", "3. Exit"]:
        print(item)


def reset_state():
    print("State reset to defaults")


show_menu()
reset_state()
reset_state()   # calling again repeats the side effect
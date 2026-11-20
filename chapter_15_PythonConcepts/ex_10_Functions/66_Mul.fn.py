# 66_Mul.fn.py
# Function type 1: no parameters and no return value. The function is defined
# once and called four times to show it is reusable.
# Type 1 - No return type and no parameters. 


# Step 1 - Declare / Define
def greet():
    print("Hi")

# Step 2 - Calling
greet()
greet()
greet()
greet()

# More complex: a no-return, no-parameter function that does real work -
# it prints a fixed banner, and its return value is None.
def print_banner():
    line = "=" * 30
    print(line)
    print("  TEST RUNNER v1.0")
    print(line)


result = print_banner()
for _ in range(2):
    print_banner()

print("The function returned:", result)  # None
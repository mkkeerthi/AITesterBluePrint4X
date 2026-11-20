# 70_Type3.py
# Function type 3: takes two parameters but returns nothing; it just prints them.
def sum_of_two(a, b):
    print(a,b)


sum_of_two(4, 5)

# More complex: type 3 formatting the arguments into a report line, and
# confirming the return value is None.
def log_result(test_name, status):
    print(f"[{status.upper():<4}] {test_name}")


log_result("login", "pass")
log_result("checkout", "fail")

# Because nothing is returned, the function's value is None.
outcome = log_result("search", "pass")
print("Returned:", outcome)

# Multiple arguments of any type are fine.
def show_pairs(*items):
    print(" | ".join(str(item) for item in items))


show_pairs("name", "pramod", 30, True)
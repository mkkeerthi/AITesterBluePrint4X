# 009_Ind.py
# Minimal example: stores a string in a long, descriptive variable name and prints it.
long_var_name_is_created_here = "Hello"
print(long_var_name_is_created_here)

# More complex: descriptive names that make code readable without comments.
# Each name says what it holds, which is what good naming is about.
max_retry_count = 3
current_retry_count = 1
is_test_environment = True
base_api_url = "https://api.example.com"

while current_retry_count <= max_retry_count:
    print(f"Attempt {current_retry_count} against {base_api_url}")
    current_retry_count += 1

# Indentation (4 spaces) defines blocks in Python - it is not optional.
if is_test_environment:
    print("Pointing at the test environment")
    print("This line is inside the if-block")
print("This line is outside the if-block")
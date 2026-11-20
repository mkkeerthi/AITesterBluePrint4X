# 21_UI.py
# Shows user input: input() prompts the user and returns whatever they type
# as a string, which is then printed back.
name = input("Enter your name")
print(name)

# More complex: input() always returns a string, so collect and convert.
# (Uncommented lines below read real input; the fallback keeps the file runnable.)
# age = int(input("Enter your age: "))
# height = float(input("Enter your height in metres: "))

age = 30
height = 1.75

# Validate before using it, then format the result.
if age <= 0:
    print("Age must be positive")
else:
    print(f"{name} is {age} years old and {height} m tall")
    print(f"Age in months: {age * 12:,}")

# Reading several comma-separated values in one go.
# raw = input("Enter numbers separated by commas: ")
raw = "10, 20, 30"
numbers = [int(part.strip()) for part in raw.split(",")]
print("Parsed:", numbers, "Total:", sum(numbers))
# 26_Literals.py
# Shows the different kinds of Python literals: integers written in decimal,
# binary (0b), octal (0o) and hexadecimal (0x), plus float, string, bool and complex.
# decimal system ->  base  -> 10
age = 89

# binary - base system ->  2
binary_number = 0b1010 # -> # 10 decimal system

# Octal  -> base 8
o = 0o130

# Hex  -> base 16
d = 0x12c

pi = 3.14  # float

# String , str
name = "Pramod"

is_pramod_married = True  # bool

# complex
complex_number = 1 + 7j

# More complex: convert between the bases and see that they are just numbers.
for value in [binary_number, o, d]:
    print(f"{value:<5} bin={bin(value):<10} oct={oct(value):<8} hex={hex(value):<8}")

# int() can parse a numeric string in a chosen base.
print(int("1010", 2))
print(int("130", 8))
print(int("12c", 16))

# Underscores and numeric separators in literals.
population = 1_400_000_000
print(population)

# Floats also accept exponent notation.
print(1.5e3, 2E-3)
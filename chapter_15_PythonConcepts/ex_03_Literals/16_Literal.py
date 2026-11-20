# 16_Literal.py
# A minimal introduction to literals: an integer, a string and a boolean
# value assigned to variables.
age = 20
name = "Pramod"
b = True

# More complex: a literal of every main kind, with its type printed.
decimal_int = 42
binary_int = 0b101010          # 42 in binary
octal_int = 0o52               # 42 in octal
hex_int = 0x2A                 # 42 in hex
floating = 3.14159
scientific = 1.5e3             # 1500.0
text = "test"
flag = False
nothing = None
complex_value = 3 + 4j
collection = [1, 2, 3]

literals = [decimal_int, binary_int, octal_int, hex_int, floating,
            scientific, text, flag, nothing, complex_value, collection]

for value in literals:
    print(f"{str(value):<14} -> {type(value).__name__}")

# Numeric literals can also use underscores for readability.
big_number = 1_000_000
print(big_number, big_number == 1000000)

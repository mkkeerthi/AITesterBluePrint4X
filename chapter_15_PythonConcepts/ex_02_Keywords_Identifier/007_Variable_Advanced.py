# 007_Variable_Advanced.py
# Creates variables of several types and prints their types with type().
# Also shows complex numbers and accessing their real and imaginary parts.
_pramod = "amit"
_abc = 23
pi = 3.14
name = "Pramod"
isMale = True

# Type
print(type(_pramod))
print(type(pi))
print(type(isMale))

complex_number = 2 + 3j
print(complex_number)
print(complex_number.real)
print(complex_number.imag)
print(type(complex_number))

# More complex: arithmetic with complex numbers and mixed-type containers.
first = 2 + 3j
second = 1 - 4j
print("Sum:", first + second)
print("Product:", first * second)
print("Magnitude:", abs(first))  # sqrt(2^2 + 3^2)

# A list can hold different types; type() reports each one.
mixed = [42, 3.14, "pramod", True, 1 + 2j, None]
for value in mixed:
    print(f"{str(value):<12} -> {type(value).__name__}")
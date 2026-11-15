# 007_Varaible_P2.py
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
# 34_P_Op.py
# Demonstrates the power (exponent) operator ** by squaring/cubing 2.
print(2 ** 2)  # ** - power
print(2 ** 3)  # ** - power
print(2 ** 4)  # ** - power

# More complex: negative and fractional exponents, plus precedence.
print(2 ** -1)          # 0.5 - reciprocal
print(9 ** 0.5)         # 3.0 - square root
print(27 ** (1 / 3))    # cube root
print(-2 ** 2)          # -(2 ** 2) = -4, power binds tighter than unary minus
print((-2) ** 2)        # 4, brackets change it

# Right-associative: 2 ** 3 ** 2 = 2 ** 9
print(2 ** 3 ** 2)

# A realistic use: compound growth (10% per year for 5 years).
principal = 1000
rate = 1.10
years = 5
print(f"Future value: {principal * rate ** years:.2f}")

# pow() is the function form, and takes an optional modulus.
print(pow(2, 10), pow(2, 10, 7))
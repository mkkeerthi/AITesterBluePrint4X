# 011_IQ.py
# Evaluates an arithmetic expression (10 + 34 * 3 - 1) to show that Python
# follows operator precedence (BODMAS): multiplication happens before + and -.
a = 10 + 34 * 3 - 1
print(a)


# BODMAS
#
# BODMAS is an acronym that helps remember the order of operations in mathematics:
# B: Brackets
# O: Order of powers or roots
# D: Division
# M: Multiplication
# A: Addition
# S: Subtraction

# More complex: brackets change the result, and ** (power) runs before * /.
plain = 2 + 3 * 4 ** 2          # 2 + 3 * 16 = 2 + 48 = 50
bracketed = (2 + 3) * 4 ** 2    # 5 * 16 = 80
left_to_right = 100 / 10 / 2    # (100 / 10) / 2 = 5.0
floor_first = 100 // 10 / 2     # (100 // 10) / 2 = 5.0

print(plain)
print(bracketed)
print(left_to_right)
print(floor_first)

# A realistic check: percentage change in a test metric.
old_value = 80
new_value = 100
percent_change = (new_value - old_value) / old_value * 100
print(f"Change: {percent_change:.1f}%")
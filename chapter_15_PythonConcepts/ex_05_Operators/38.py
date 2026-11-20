# 38.py
# Shows logical or (True if either operand is True) and logical and
# (True only if both operands are True) on boolean values.
f = False
t = True
print(f or t)
print(f and t)

# More complex: all four combinations in a truth table, then a realistic
# permission check built from or/and.
print("a     b     a or b   a and b")
for a in (False, True):
    for b in (False, True):
        print(f"{a!s:<5} {b!s:<5} {str(a or b):<8} {a and b}")

is_admin = False
is_owner = True
can_edit = is_admin or is_owner
can_delete = is_admin and is_owner
print("Can edit:", can_edit)
print("Can delete:", can_delete)

# or is commonly used to supply a default value.
username = ""
display_name = username or "Guest"
print(display_name)
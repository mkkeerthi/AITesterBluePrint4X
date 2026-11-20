# 62_Pass.py
# Shows pass (a no-op placeholder): prints only 5 and 6, doing nothing for
# every other number.
for i in range(0, 10, 1):
    if i == 6 or i == 5:
        print(i)
    else:
        pass # do nothing

# More complex: pass as a placeholder in functions and classes you will
# fill in later, and to deliberately ignore an exception.
def not_implemented_yet():
    pass  # keeps the syntax valid while the body is empty


class EmptyConfig:
    pass


print(not_implemented_yet())
print(EmptyConfig())

# Pass is also a way to say "ignore this case on purpose".
for value in [1, "two", 3]:
    if isinstance(value, str):
        pass  # not interested in strings here
    else:
        print("number:", value * 2)

try:
    risky = 1 / 0
except ZeroDivisionError:
    pass  # intentionally swallowed in this demo
print("continued after the error")
# 006_Identifier.py
# Shows Python identifier naming rules: names may start with a letter or
# underscore but not a digit (123abc is invalid), and underscore is a valid name.
age = 65
_age = 65
print(age)
print(_age)

_ = 12
print(_)
_ = _ + 1
print(_)

# 123abc = 90
abc123 = "abc123"
print(abc123)
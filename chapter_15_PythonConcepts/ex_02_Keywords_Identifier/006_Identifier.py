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

# More complex: validate identifier names programmatically.
# identifier.isidentifier() checks naming rules, iskeyword() checks reserved words.
import keyword


def describe(name):
    if not name.isidentifier():
        return "INVALID (bad characters or starts with a digit)"
    if keyword.iskeyword(name):
        return "INVALID (reserved keyword)"
    return "VALID"


for candidate in ["total_marks", "2fast", "my-var", "class", "_private", "userName"]:
    print(f"{candidate:<12} -> {describe(candidate)}")

# Style convention (PEP 8): snake_case for variables and functions.
test_case_count = 12
print(test_case_count)
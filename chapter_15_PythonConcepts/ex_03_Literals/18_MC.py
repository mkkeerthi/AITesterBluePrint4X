# 18_MC.py
# Shows an inline comment (after a statement) plus a multi-line triple-quoted
# comment used as a file/topic header, then prints the variable.
age = 65  # int
"""
This is multi comment
1. Author- Pramod Dutta
2. Information
3. Print the age of pramod
"""
print(age)

# More complex: inline comments annotating a small config, plus a short
# module docstring describing what the script does.
"""Test configuration used by the examples below."""

BASE_URL = "https://api.example.com"  # str literal
TIMEOUT_SECONDS = 30                  # int literal
RETRY_LIMIT = 3                       # int literal
VERIFY_SSL = True                     # bool literal
SUPPORTED_METHODS = ("GET", "POST")   # tuple literal

config = {
    "base_url": BASE_URL,
    "timeout": TIMEOUT_SECONDS,
    "retry": RETRY_LIMIT,
    "verify": VERIFY_SSL,
}

for key, value in config.items():
    print(f"{key:<10} = {value!r}")  # !r shows the repr, so types are visible
# 27_Literal_ESCAPE.py
# Demonstrates escape sequences inside strings: \n (new line), \t (tab) and
# \b (backspace), showing how they change the printed output.
# Escape Sequence
# \n -> new line
# \t -> tab
# \b -> backspace (1 char backspace)

print("Hello\nWorld")
print("Hello\tWorld")
print("Hello\bWorld")

# More complex: the remaining common escapes (quotes, backslash, bell).
print("He said: \"run the tests\"")     # escaped quotes
print("Item\tPrice")
print("Pen\t20")
print("Backslash: C:\\temp\\report.txt") # escaped backslash
print("Notification beep: \a")          # bell (may be silent in some terminals)
print("Next line starts here\n")

# A raw string keeps every backslash, which is ideal for paths and regex.
print(r"C:\pramod\n.txt")

# Triple-quoted strings keep their newlines exactly as written.
report = """Test Summary
Passed: 12
Failed: 0
"""
print(report)
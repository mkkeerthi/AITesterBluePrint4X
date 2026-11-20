# 164.py
# Demonstrates a SyntaxError: "while True print(...)" is missing the colon, so
# the file cannot even be parsed (note the comment on line 2 is not valid syntax either).
# A SyntaxError stops the file from being parsed, so the broken form is kept
# as a string and compiled below rather than written as real code:
broken = 'while True print("Hello World!")'
# SyntaxError: invalid syntax

# More complex: detect the syntax problem safely with compile(), then show the
# corrected version.
try:
    compile(broken, "<string>", "exec")
except SyntaxError as error:
    print("SyntaxError:", error.msg, "| line", error.lineno, "| offset", error.offset)

# The correct version of the line above:
while True:
    print("Hello World!")
    break            # added so the loop ends

# compile() can then run validated source with exec().
good_code = "result = sum(range(5))\nprint('exec result:', result)"
exec(compile(good_code, "<string>", "exec"))

# IndentationError and TabError are subclasses of SyntaxError.
try:
    compile("if True:\nprint('bad')", "<string>", "exec")
except IndentationError as error:
    print("IndentationError:", error.msg)

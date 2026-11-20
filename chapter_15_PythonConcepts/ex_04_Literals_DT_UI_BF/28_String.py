# 28_String.py
# Compares single vs double quoted strings, then uses a raw string (r"...")
# so backslash escape sequences such as \n in a Windows path are printed literally.
c = 'C'
c1 = "C"
print(c)
print(c1)

# dir = 'C:\pramod\n.txt'
dir = r"C:\pramod\n.txt" # raw - it will print as it is (ignore the escape seq.)
print(dir)

# More complex: show what happens WITHOUT the raw prefix, then f-string and
# multi-line variants side by side.
print("line one\nline two")       # \n becomes a newline
print(repr("line one\nline two")) # repr makes the difference visible
print(repr(r"line one\nline two"))

folder = "pramod"
file_name = "notes.txt"
print(rf"C:\{folder}\{file_name}")  # raw + f-string together

# Triple quotes let a string span lines without \n escapes.
query = """SELECT id, name
FROM users
WHERE active = 1"""
print(query)
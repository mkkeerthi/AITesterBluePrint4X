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
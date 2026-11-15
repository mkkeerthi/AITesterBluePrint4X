# 173_FIO.py
# File I/O exception handling: tries to read a JSON test-data file and catches
# FileNotFoundError, printing the OS error message if the file is missing.
try:
    data = open("09_Exceptions/test.json").read()
    print(data)
except FileNotFoundError as fnf:
    print(fnf)
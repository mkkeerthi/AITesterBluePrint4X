# 173_FileIO.py
# File I/O exception handling: tries to read a JSON test-data file and catches
# FileNotFoundError, printing the OS error message if the file is missing.
try:
    data = open("09_Exceptions/test.json").read()
    print(data)
except FileNotFoundError as fnf:
    print(fnf)

# More complex: read JSON safely, handle every expected failure, and always
# close the file with `with`. Creates its own test file so it runs anywhere.
import json
import os
import tempfile

path = os.path.join(tempfile.gettempdir(), "test_173.json")

with open(path, "w", encoding="utf-8") as handle:
    json.dump({"tests": [{"name": "login", "status": "PASS"}]}, handle)

try:
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
except FileNotFoundError:
    print("file is missing")
except json.JSONDecodeError as error:
    print(f"invalid JSON: {error}")
except PermissionError:
    print("no permission to read the file")
else:
    print("loaded:", data)
    print("first test:", data["tests"][0]["name"])
finally:
    if os.path.exists(path):
        os.remove(path)

# Different modes in one place:
# "r" read, "w" write (truncate), "a" append, "x" create new (fails if exists)
append_path = os.path.join(tempfile.gettempdir(), "test_173_append.txt")
try:
    with open(append_path, "w") as f:
        f.write("line 1\n")
    with open(append_path, "a") as f:
        f.write("line 2\n")
    with open(append_path) as f:
        print("lines:", f.read().splitlines())
    try:
        with open(append_path, "x") as f:
            pass
    except FileExistsError as error:
        print("FileExistsError:", error)
finally:
    if os.path.exists(append_path):
        os.remove(append_path)
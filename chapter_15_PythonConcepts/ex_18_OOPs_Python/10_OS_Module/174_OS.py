# 174_OS.py
# Tour of the os module: prints the OS name, current working directory and
# directory contents, and demonstrates creating, removing and renaming files/folders.
import os
print(os.name)
print(os.getcwd())
# print(os.mkdir("AI"))
print(os.listdir())

print(os.remove("AI.txt"))
print(os.rename("AI.txt","testdata.txt"))


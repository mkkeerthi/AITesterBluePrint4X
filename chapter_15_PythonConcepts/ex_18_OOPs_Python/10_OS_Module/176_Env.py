# 176_Env.py
# Reads an environment variable with os.getenv(): prints the value of TOKEN
# (or None if it is not set), the usual way to keep secrets out of code.
import os
print( os.getenv("TOKEN"))
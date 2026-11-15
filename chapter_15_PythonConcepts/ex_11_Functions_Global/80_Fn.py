# 80_Fn.py
# Explains variable scope: a module-level (global) variable is readable inside
# a function, but a variable created inside the function is local and is not
# accessible outside it (hence the NameError if the last line is uncommented).
pb_global_b = 12

def my_function():
    pb_a = 10
    print(pb_a)
    print(pb_global_b)


print(pb_global_b)
# print(pb_a) # NameError: name 'pb_a' is not defined
my_function()
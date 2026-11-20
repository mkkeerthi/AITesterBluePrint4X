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

# More complex: reading a global is fine, but assigning one inside a function
# creates a NEW local unless you declare it global.
counter = 0


def increment_wrong():
    counter = 10        # this is a local variable, not the global
    print("inside (local):", counter)


def increment_right():
    global counter
    counter += 1        # this really changes the module-level variable


increment_wrong()
print("global after wrong:", counter)
increment_right()
increment_right()
print("global after right:", counter)

# globals() lets you inspect the module-level names.
print("pb_global_b in globals():", "pb_global_b" in globals())
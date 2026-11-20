# 67_Arg_Para.Fn.py
# Distinguishes a parameter (the name in the function definition) from an
# argument (the actual value passed in when calling), calling greet() with two types.
def greet(name): # parameter when define.
    print("Hi", name)


greet("pramod") # when argument is call the fn
greet(3.14)

# parameter vs Argument

# More complex: two parameters, passed positionally and by keyword, with
# the argument count enforced by Python itself.
def greet_full(first_name, last_name):
    print(f"Hi, {first_name} {last_name}")


greet_full("Pramod", "Dutta")            # positional
greet_full(last_name="Dutta", first_name="Pramod")  # keyword

# Calling with the wrong number of arguments raises a TypeError:
# greet_full("Pramod")  -> missing 1 required positional argument

# The argument type is not enforced - it is whatever object was passed.
for argument in ["text", 42, 3.14, None]:
    greet(argument)
    print("  received a", type(argument).__name__)
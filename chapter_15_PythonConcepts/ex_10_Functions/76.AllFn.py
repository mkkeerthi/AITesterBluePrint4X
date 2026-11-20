# 76.AllFn.py
# A catalog of function styles in one file: built-in functions, no-return/no-param,
# argument-only, default arguments, and arguments-with-return-type variants.
import math

# built in functions
result = max(3, 4)
print(result)

# 1. They can't return -> non return
# No Return Type and No Parameter / Argument - NRNP

def greet():
    print("Hello")

greet()

# 2. # No Return Type and with Argument/ Param
def greet_by_name(name):
    print("Hello,", name)


greet_by_name("Pramod")

# 3. No Return Type and with Default Argument ( # positional argument)
def say_hello_default_arg(name="Pramod"):
    print("Hello", name.upper())


say_hello_default_arg("Dutta")
say_hello_default_arg()


def multiple_args(name1="A", name2="B"):
    print("Mul -> ", name1, name2)


multiple_args()
multiple_args("Lucky", "Sharma")
multiple_args(name1="Pramod")
multiple_args(name1="Dutta", name2="Amit")
multiple_args(name2="Amit")


# def test(name):
#     return name
# test("test")


# 4. Argument + return Type

def sum_of_two(a, b):
    return a + b


result = sum_of_two(4, 56)
print(result)


def sum_of_two_number_with_default(num1=100, num2=200):
    print("I will sum the two numbers!")
    return num1 + num2


result = sum_of_two_number_with_default(num1=34, num2=34)
print(result)
result = sum_of_two_number_with_default()
print(result)

# More complex: one function that combines everything - required, default,
# *args and **kwargs - the most flexible signature Python allows.
def run_suite(name, *cases, env="dev", **options):
    print(f"Suite: {name} (env={env}, timeout={options.get('timeout', 30)}s)")
    for case in cases:
        print("  -", case)
    if options.get("verbose"):
        print("  options:", options)


run_suite("smoke", "login", "logout")
run_suite("regression", "search", "checkout", env="qa", timeout=60, verbose=True)

# Order rules for a signature: positional, default, *args, then **kwargs.
# A function can also be passed around like any other value.
operations = {"add": sum_of_two, "mul": lambda a, b: a * b}
for label, fn in operations.items():
    print(f"{label}(3, 4) = {fn(3, 4)}")
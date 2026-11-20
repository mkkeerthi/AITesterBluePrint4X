# 78_Infinite_Arg.py
# Shows *args: the function accepts any number of positional arguments, which
# arrive as a tuple that is looped over and printed.
def print_mul_arg(*pramod_list):
    # args - List
    for i in pramod_list:
        print(i)


print_mul_arg("pramod")
print_mul_arg(2, 3, 1, 4, 3, 2, 2, 2, 2, 2, 2)
print_mul_arg("pramod", "dutta")
print_mul_arg("pramod", "dutta", "third")
print_mul_arg("pramod", "dutta", "third", 3.14)
print_mul_arg("pramod", "dutta", "third", 3.14, True)

# More complex: *args used for numeric work, combined with a fixed parameter
# and **kwargs for options.
def total(*numbers, start=0, scale=1):
    return start + sum(n * scale for n in numbers)


print(total(1, 2, 3))
print(total(1, 2, 3, start=10))
print(total(1, 2, 3, scale=2))

# * unpacks a sequence into positional arguments at the call site.
values = [5, 10, 15]
print(total(*values))

# Joining *args with a separator, showing the tuple type.
def label_all(prefix, *args):
    print(type(args).__name__, args)
    return " ".join(f"{prefix}:{item}" for item in args)


print(label_all("tag", "a", "b", "c"))
print(label_all("tag"))

# **kwargs collects unexpected keyword arguments into a dict.
def describe(**details):
    for key, value in details.items():
        print(f"{key} = {value}")


describe(env="qa", browser="chrome", headless=True)
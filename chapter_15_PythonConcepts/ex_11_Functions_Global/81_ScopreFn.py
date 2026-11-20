# 81_ScopreFn.py
# Compares scopes: the module-level "public_toilet" is visible inside every
# function, while "private_toilet" defined inside home() is local to it.
public_toilet = "PB"


def home():
    private_toilet = "PT"
    print(public_toilet)
    print(private_toilet)

def stranger():
    print(public_toilet)
    # print(private_toilet)


    

# More complex: actually call the functions, and show LEGB lookup in action.
home()
stranger()

# LEGB: Local -> Enclosing -> Global -> Built-in. Python stops at the first
# scope that defines the name, so a local shadows everything above it.
name = "global"


def outer():
    name = "enclosing"

    def inner():
        name = "local"
        print("inner sees:", name)

    inner()
    print("outer sees:", name)


outer()
print("module sees:", name)

# Without a local assignment, the global is visible from any depth.
def read_only():
    print("read_only sees:", public_toilet)


read_only()
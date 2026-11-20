# 84_Deco_Imp.py
# Demonstrates a decorator with a driving analogy: add_security() wraps another
# function in a wrapper() that runs code before and after it, and is applied
# with @add_security to drive_ola_scooter().
def add_security(func):
    def wrapper():
        print("1.Before the function is called.")
        print("2.Add Helmet, Dashcash, gloves, knee guards, License")
        func()
        print("3.After the function is called.")
        print("4.Secure Driving, Leave all the items")

    return wrapper


@add_security
def drive_ola_scooter():
    print("I am driving ola scooter")


drive_ola_scooter()

# More complex: a decorator that accepts arguments and passes them through
# with *args/**kwargs, so it works on any function signature.
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"-> calling {func.__name__} with {args} {kwargs}")
        result = func(*args, **kwargs)
        print(f"<- {func.__name__} returned {result!r}")
        return result
    return wrapper


@log_calls
def add(a, b):
    return a + b


@log_calls
def sign_in(user, remember=False):
    return f"{user} signed in (remember={remember})"


print(add(2, 3))
print(sign_in("pramod", remember=True))

# functools.wraps preserves the original function's name and docstring.
import functools


def preserve(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@preserve
def documented():
    """This docstring survives decoration."""
    return "ok"


print(documented.__name__, "|", documented.__doc__)

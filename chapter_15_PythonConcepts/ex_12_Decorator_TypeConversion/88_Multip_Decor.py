# 88_Multip_Decor.py
# Multiple decorators on one function. decorator1 and decorator2 are stacked on
# say_hello; decorators apply bottom-up, so decorator2's output prints first.
def decorator1(func):
    def wrapper():
        print("Decorator 1")
        func()
    return wrapper

def decorator2(func):
    def wrapper():
        print("Decorator 2")
        func()
    return wrapper


@decorator1
@decorator2
def say_hello():
    print("Hello!")


say_hello()
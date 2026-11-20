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

# More complex: decorators with arguments are a function returning a
# decorator. This is the pattern behind @pytest.mark.skipif etc.
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


def bold(func):
    def wrapper(*args, **kwargs):
        return f"**{func(*args, **kwargs)}**"
    return wrapper


@repeat(3)
@bold
def announce(message):
    print("announcing:", message)
    return message


print(announce("release"))

# Two decorators where order changes the meaning: bold then repeat vs
# the reverse gives a different number of wrapped calls.
@bold
@repeat(2)
def title(text):
    return text


print(title("hello"))
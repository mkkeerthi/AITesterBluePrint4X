# 82_Nested_Fn.py
# Shows nested functions and closure-like scope: an inner function can read the
# outer function's variable, and a local variable with the same name shadows it.
def outer_function():
    var1 = 30 # local

    def inner_function():
        var2 = 90
        print(var1)

    def inner_function2():
        var1 = 100
        print(var1)
        # print(var2)


    inner_function()
    inner_function2()

outer_function()

# More complex: a real closure - the inner function keeps access to the outer
# function's variables even after the outer function has returned.
def make_multiplier(factor):
    def multiply(value):
        return value * factor
    return multiply


double = make_multiplier(2)
triple = make_multiplier(3)
print(double(10), triple(10))

# nonlocal lets the inner function REASSIGN an enclosing variable.
def make_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment


tick = make_counter()
print(tick(), tick(), tick())

# Another counter shares nothing with the first - each closure has its own state.
other_tick = make_counter()
print(other_tick())
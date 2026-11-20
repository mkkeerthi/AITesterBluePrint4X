# 146_MLoading.py
# Demonstrates that Python has no true method overloading: defining add() twice
# simply replaces the first definition (the 3-argument version is commented out).
class MathClass:
    def add(self, a,b):
        return a+b

    # def add(self,a,b,c):
    #     return a-b-c

# More complex: prove only the last definition survives, then show the three
# real ways Python achieves overload-like behaviour.
obj = MathClass()
print("only the last definition exists:", obj.add(2, 3))

# 1. Default arguments cover the optional-argument case.
class WithDefaults:
    def add(self, a, b, c=0):
        return a + b + c


print(WithDefaults().add(1, 2), WithDefaults().add(1, 2, 3))

# 2. *args handles a truly variable number of arguments.
class WithVarargs:
    def add(self, *numbers):
        return sum(numbers)


w = WithVarargs()
print(w.add(1), w.add(1, 2), w.add(1, 2, 3, 4))

# 3. Type dispatch covers different TYPES with the same name.
from functools import singledispatchmethod


class Dispatcher:
    @singledispatchmethod
    def describe(self, value):
        return f"something: {value}"

    @describe.register
    def _(self, value: int):
        return f"integer: {value}"

    @describe.register
    def _(self, value: str):
        return f"text: {value!r}"


d = Dispatcher()
print(d.describe(42), "|", d.describe("hi"), "|", d.describe(3.5))
# 148_REAL_Mloading.py
# Realistic overload-like behavior using a default argument (c=10): the second
# add() definition wins, yet it can be called with two or three arguments.
class MathClass:
    def add(self, a, b):
        return a + b

    def add(self, a, b, c=10):
        return a + b + c


obj_ref = MathClass()
print(obj_ref.add(3, 4, 5))
print(obj_ref.add(3.14, 4.14))

# More complex: a version where the "overload" is explicit and safe - the
# default is None so you can tell whether the third value was supplied.
class Calculator:
    def add(self, a, b, c=None):
        if c is None:
            return a + b
        return a + b + c

    def add_many(self, *numbers):
        return sum(numbers)


calc = Calculator()
print(calc.add(2, 3))            # 5
print(calc.add(2, 3, 4))         # 9
print(calc.add(2, 3, c=0))       # 5 - explicitly passed zero, still adds it
print(calc.add_many(1, 2, 3, 4))

# Why default=10 in the original is dangerous: you cannot tell "not given"
# from "given as 10". None as the sentinel removes the ambiguity.
class Ambiguous:
    def add(self, a, b, c=10):
        return a + b + c


print("ambiguous:", Ambiguous().add(1, 2))       # 13 - surprising
print("explicit:", Calculator().add(1, 2))       # 3 - clear
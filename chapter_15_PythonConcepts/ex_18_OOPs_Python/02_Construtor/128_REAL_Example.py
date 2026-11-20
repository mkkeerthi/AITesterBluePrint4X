# 128_REAL_Example.py
# Practical class example: Calc has a default constructor and four methods
# (sum, sub, mul, div). Two numbers are read from the user, and every operation
# is run on one Calc object.
class Calc:
    a = None
    b = None

    def __init__(self):
        print("DC")

    def sum(self, a, b):
        return a+b
    
    def sub(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b

    def div(self, a, b):
        return a / b

a = float(input("Enter the value of a"))
b = float(input("Enter the value of b"))

object_ref = Calc()

output_sum = object_ref.sum(a, b)
output_sub = object_ref.sub(a, b)
output_mul = object_ref.mul(a, b)
output_div = object_ref.div(a, b)
print(output_sum, output_sub, output_mul, output_div)

# More complex: a version that stores the operands on the object (no
# parameters needed per call), guards division by zero, and keeps history.
class Calculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.history = []

    def _record(self, label, value):
        self.history.append(f"{label}: {value}")
        return value

    def sum(self):
        return self._record("sum", self.a + self.b)

    def div(self):
        if self.b == 0:
            return self._record("div", "undefined (division by zero)")
        return self._record("div", round(self.a / self.b, 4))

    def report(self):
        return "\n".join(self.history)


calc = Calculator(10, 0)
print(calc.sum())
print(calc.div())
print(calc.report())

print(Calculator(10, 4).div())
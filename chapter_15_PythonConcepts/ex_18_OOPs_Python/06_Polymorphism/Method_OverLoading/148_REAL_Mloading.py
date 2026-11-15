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
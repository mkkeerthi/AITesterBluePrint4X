# 146_MLoading.py
# Demonstrates that Python has no true method overloading: defining add() twice
# simply replaces the first definition (the 3-argument version is commented out).
class MathClass:
    def add(self, a,b):
        return a+b

    # def add(self,a,b,c):
    #     return a-b-c
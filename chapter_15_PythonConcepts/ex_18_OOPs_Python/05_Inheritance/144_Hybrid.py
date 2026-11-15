# 144_Hybrid.py
# Hybrid inheritance - a mix of multiple and multilevel inheritance: A and B
# both extend Base, and C extends both A and B, so C can call all four methods.
#Hybrid Inheritance
#A mix of multiple and multilevel inheritance.
class Base:
    def base_method(self):
        print("Base method")

class A(Base):
    def a_method(self):
        print("A method")

class B(Base):
    def b_method(self):
        print("B method")

class C(A, B):
    def c_method(self):
        print("C method")

obj = C()
obj.base_method()
obj.a_method()
obj.b_method()
obj.c_method()
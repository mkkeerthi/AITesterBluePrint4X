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

# More complex: diamond inheritance with a shared constructor. super() walks
# the MRO, so Base.__init__ runs exactly once.
class Base2:
    def __init__(self):
        print("Base2 init")
        self.base_ready = True


class A2(Base2):
    def __init__(self):
        print("A2 init")
        super().__init__()
        self.a_ready = True


class B2(Base2):
    def __init__(self):
        print("B2 init")
        super().__init__()
        self.b_ready = True


class C2(A2, B2):
    def __init__(self):
        print("C2 init")
        super().__init__()


c = C2()
print("all initialised:", c.a_ready, c.b_ready, c.base_ready)
print("MRO:", [cls.__name__ for cls in C2.__mro__])
print("Base2 only appears once:", C2.__mro__.count(Base2))

# Without cooperative super(), Base.__init__ can run twice or not at all.
class A3(Base2):
    def __init__(self):
        Base2.__init__(self)


class B3(Base2):
    def __init__(self):
        Base2.__init__(self)


class C3(A3, B3):
    def __init__(self):
        A3.__init__(self)
        B3.__init__(self)      # Base2 init printed twice


print("--- non-cooperative version ---")
C3()
# 157_Static.py
# Explains static/class members: statcousreName and mentor belong to the class
# and are shared by all objects, while name is per-object. display2() is a
# @staticmethod that needs no self and is called on the class itself.
# Static = Belong to class
#. it will be same for all objects ref.
# whatever is common b/w all objects ref
# it become static

class AITB:
    statcousreName  = "AITB"
    mentor = "PrrammodDutta"

    def __init__(self,name):
        self.name = name

    def display(self):
        print("Hi,", self.name,"Your Mentor is " + AITB.mentor)

    @staticmethod
    def display2():
        print("Static Method!")

s1 = AITB("Amit")
s2 = AITB("Lucky")

s1.display()
s2.display()

AITB.display2()

# More complex: the difference between @staticmethod and @classmethod, and
# proof that static methods need neither self nor cls.
class AITB2:
    course = "AITB"
    mentor = "Pramod"
    student_count = 0

    def __init__(self, name):
        self.name = name
        AITB2.student_count += 1

    def display(self):
        print(f"{self.name} -> {AITB2.mentor}")

    @staticmethod
    def is_valid_name(name):
        # No access to the class or the instance - pure utility.
        return isinstance(name, str) and len(name.strip()) > 1

    @classmethod
    def from_full_name(cls, full_name):
        first = full_name.split()[0]
        return cls(first)

    @classmethod
    def info(cls):
        return f"{cls.course}: {cls.student_count} student(s)"


print(AITB2.is_valid_name("Amit"), AITB2.is_valid_name(""))
s3 = AITB2.from_full_name("Navita Sharma")
s3.display()
print(AITB2.info())

# Where static and class methods live in the namespace:
print("static in __dict__:", type(AITB2.__dict__["is_valid_name"]).__name__)
print("classmethod in __dict__:", type(AITB2.__dict__["info"]).__name__)

# A static method can also be called on an instance - same function either way.
print(s3.is_valid_name("Ravi"))
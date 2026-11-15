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
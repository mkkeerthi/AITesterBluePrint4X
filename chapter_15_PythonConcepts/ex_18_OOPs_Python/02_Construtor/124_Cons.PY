# 124_Cons.PY
# Constructor basics: MobilePhone defines __init__ (called automatically when
# the object is created) plus a normal method talk(). Creating iphone runs
# __init__ and prints the message; talk() is not called here.
class MobilePhone:
    model = None

    def __init__(self):
        print("I will be called, when obj is created!")

    def talk(self):
        print("Normal F(n)")

iphone = MobilePhone()
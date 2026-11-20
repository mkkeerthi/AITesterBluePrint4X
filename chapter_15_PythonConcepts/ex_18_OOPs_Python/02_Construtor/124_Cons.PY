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

# More complex: a constructor that takes arguments, sets defaults and
# validates them; two objects show independent state.
class Laptop:
    def __init__(self, brand, ram_gb=8):
        if ram_gb <= 0:
            raise ValueError("RAM must be positive")
        self.brand = brand
        self.ram_gb = ram_gb
        print(f"created {self.brand} with {self.ram_gb} GB")

    def talk(self):
        print(f"{self.brand} is running")

    def __str__(self):
        return f"Laptop({self.brand}, {self.ram_gb}GB)"


mac = Laptop("MacBook", 16)
thinkpad = Laptop("ThinkPad")

mac.talk()
thinkpad.talk()
print(mac)
print([mac, thinkpad])

# The constructor runs once per object, so the message printed twice above.
print("instances made:", Laptop.__name__)
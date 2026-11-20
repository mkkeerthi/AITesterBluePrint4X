# 123_Create_Class.py
# A minimal class with a class attribute (model) and a method. An object is
# created, its attribute is set, and the method is called. Note: talk() lacks
# self, so calling it raises a TypeError in Python 3.
class MobilePhone:
    model = None

    def talk():
        print("Hello")


ipone = MobilePhone()
ipone.model = "iphone 18 Pro Max"
try:
    ipone.talk()
except TypeError as error:
    print("TypeError:", error)

# More complex: the correct signature (self) plus instance data, so the
# method can actually read the object's own attributes.
class Laptop:
    brand = None

    def __init__(self, brand, ram_gb):
        self.brand = brand
        self.ram_gb = ram_gb

    def talk(self):
        print(f"{self.brand} says hello ({self.ram_gb} GB RAM)")

    def boot(self, os_name="Linux"):
        return f"{self.brand} booting {os_name}"


my_laptop = Laptop("ThinkPad", 16)
my_laptop.talk()
print(my_laptop.boot())
print(my_laptop.boot("Windows"))

# Each object keeps its own attribute values.
second = Laptop("MacBook", 32)
second.talk()
print("class attribute still:", Laptop.brand)
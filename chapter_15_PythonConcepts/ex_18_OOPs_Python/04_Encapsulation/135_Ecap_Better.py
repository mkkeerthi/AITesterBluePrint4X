# 135_Ecap_Better.py
# Explains Python's naming conventions for access levels: public (name),
# protected (_name) and private (__name, name-mangled). Reading
# object_ref.__private_baby from outside raises AttributeError; only methods
# inside the class can use it.
class Car:
    def __init__(self):
        self.public_pramod = "pramod"
        self._protected_baby = "demo123"
        self.__private_baby = "demo123"

    def nany(self):
        self.__password_yogesh_private = "345"

    def wife(self):
        print(self.__private_baby)

    def mother(self):
            print(self.__private_baby)

object_ref = Car()
print(object_ref.public_pramod)
try:
    print(object_ref.__private_baby)
except AttributeError as error:
    print("AttributeError:", error)
# object_ref.wife()
# object_ref.mother()

# More complex: see the full picture - what outside code can reach, what the
# name mangling does, and why properties are the better tool than getters.
print("public:", object_ref.public_pramod)
print("protected (convention only):", object_ref._protected_baby)

# Name mangling renames __private_baby to _Car__private_baby, which is why
# the plain attribute lookup above failed.
print("mangled access:", object_ref._Car__private_baby)

# Inside-class methods do reach the private attribute.
object_ref.wife()

# The idiomatic replacement for getters/setters is a property.
class Wallet:
    def __init__(self, balance):
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("balance cannot be negative")
        self._balance = value


w = Wallet(100)
print("read like an attribute:", w.balance)
w.balance = 150
print("after set:", w.balance)
try:
    w.balance = -5
except ValueError as error:
    print("setter rejected:", error)
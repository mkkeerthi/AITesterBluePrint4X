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
print(object_ref.__private_baby)
# object_ref.wife()
# object_ref.mother()
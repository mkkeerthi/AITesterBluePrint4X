# 122.py
# A Dog class with attributes and methods. Shows that a method uses self to
# reach the object's own data (self.name), and that Dog() creates an object
# stored in the reference variable chow.
class Dog:
    # A
    name = None
    breed = None
    height = None
    weight = None
    # B
    def bark(self):
        print("Barking")
        # print(name)
        print(self.name)

    def talk(self):
        print("Talking")


chow = Dog()

# Dog() - Object
# chow -> Object Ref
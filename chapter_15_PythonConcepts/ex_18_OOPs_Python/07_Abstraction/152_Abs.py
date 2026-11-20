# 152_Abs.py
# Introduces abstraction: ABC (abstract base class) defines what must exist
# without implementing it. Animal marks sound() with @abstractmethod, and Dog
# must provide the implementation before it can be instantiated.
# Abstraction
# Hide the details and show what is required.

# Car - with key _ __private, tyres -> public,

# Car -> multiple - Engine, GearBox
# Car -> driver -> Engine, gearbox?

from abc import ABC, abstractmethod

class Animal(ABC):

    def __init__(self,name):
        self.name = name

    @abstractmethod
    def sound(self):
        pass

class Dog(Animal):

    def sound(self):
        print("Bark!")

dog = Dog("PP")
dog.sound()

# More complex: prove the abstract class cannot be instantiated, add a
# second implementation, and include a concrete method shared by all animals.
class Cat(Animal):
    def sound(self):
        print("Meow!")


class Animal2(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def sound(self):
        ...

    def describe(self):
        # Concrete: shared by every subclass, no need to repeat it.
        return f"{self.name} says: {self.sound_text()}"

    @abstractmethod
    def sound_text(self):
        ...


class Dog2(Animal2):
    def sound(self):
        print("Bark!")

    def sound_text(self):
        return "woof"


class Cat2(Animal2):
    def sound(self):
        print("Meow!")

    def sound_text(self):
        return "meow"


Cat("tom").sound()

# Instantiating an abstract class raises TypeError.
try:
    Animal2("x")
except TypeError as error:
    print("TypeError:", error)

for pet in [Dog2("Rex"), Cat2("Tom")]:
    print(pet.describe())
    pet.sound()

# Incomplete subclasses are rejected at creation, not at call time.
class Incomplete(Animal2):
    def sound(self):
        print("?")


try:
    Incomplete("x")
except TypeError as error:
    print("still abstract:", error)
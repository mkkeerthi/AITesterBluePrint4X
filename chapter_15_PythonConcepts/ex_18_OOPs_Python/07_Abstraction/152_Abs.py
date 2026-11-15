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
# 153_Abs_Part1.py
# Abstraction part 1: abstract Father class declares loan() as abstract; the
# concrete subclass Amit implements it and can then be instantiated.
from abc import ABC,abstractmethod

class Father(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def loan(self):
        pass

class Amit(Father):

    def loan(self):
        print("Giving the 50K loan")

amit = Amit("AMIT SHARMA")
amit.loan()

# More complex: a second subclass, an abstract property, and enforcement -
# the lesson is the contract, not the implementation.
class Priya(Father):
    def loan(self):
        print(f"{self.name} gives a 30K loan")


Priya("PRIYA").loan()

# The abstract method makes Father itself unusable.
try:
    Father("nobody")
except TypeError as error:
    print("TypeError:", error)


# Abstract properties work too, and are checked the same way.
from abc import ABC, abstractmethod


class Shape(ABC):
    @property
    @abstractmethod
    def area(self):
        ...

    def __str__(self):
        return f"{type(self).__name__} with area {self.area:.2f}"


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return 3.14159 * self.radius ** 2


class Square(Shape):
    def __init__(self, side):
        self.side = side

    @property
    def area(self):
        return self.side ** 2


for shape in [Circle(2), Square(3)]:
    print(shape)
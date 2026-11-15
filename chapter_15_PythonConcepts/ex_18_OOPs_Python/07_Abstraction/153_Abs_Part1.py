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
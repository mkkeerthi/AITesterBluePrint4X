# 155_Hide_Abs.py
# "Hide the details" example: GearBox and Engine declare abstract methods, and
# Car implements them all. drive() shows only the simple interface (start,
# setGear, stop) while the internals stay hidden.
from abc import ABC, abstractmethod


class GearBox(ABC):
    @abstractmethod
    def setGear(self):
        pass

class Engine:
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass


class Car(Engine,GearBox):
    def start(self):
        print("Starting")

    def stop(self):
        print("Stop")

    def setGear(self):
        print("Gearbox is ready")

    def drive(self):
        self.start()
        self.setGear()
        self.stop()



tesla = Car()
tesla.drive()












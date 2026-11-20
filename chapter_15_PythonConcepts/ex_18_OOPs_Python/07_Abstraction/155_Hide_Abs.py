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

# More complex: a properly abstracted version. Engine is also an ABC (it was
# acting like one), and drive() takes parameters so the interface is useful.
from abc import ABC, abstractmethod


class Engine2(ABC):
    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def stop(self):
        ...


class GearBox2(ABC):
    @abstractmethod
    def set_gear(self, gear):
        ...


class Car2(Engine2, GearBox2):
    def __init__(self, model):
        self.model = model
        self.gear = 0

    def start(self):
        print(f"{self.model}: engine started")

    def stop(self):
        print(f"{self.model}: engine stopped")

    def set_gear(self, gear):
        if not -1 <= gear <= 6:
            raise ValueError("invalid gear")
        self.gear = gear
        print(f"{self.model}: gear {gear}")

    def drive(self, gear=1):
        # The public workflow. Everything above is the hidden detail.
        self.start()
        self.set_gear(gear)
        print(f"{self.model}: driving in gear {self.gear}")
        self.stop()


Car2("Tesla Model 3").drive()
Car2("Audi").drive(gear=3)

# Engine2 cannot be created directly - the abstraction is enforced.
try:
    Engine2()
except TypeError as error:
    print("TypeError:", error)












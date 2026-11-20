# 126_Param_Const.py
# Parameterized constructor: __init__(self, nameGiven, breedGiven) stores the
# arguments on the object with self, so each Dog remembers its own name/breed.
# The final Dog() call fails because this class has no no-argument constructor.
class Dog:
     # Attributes - Instance variables | Data variables
    name = None
    breed = None
    height = None
    weight = None
    race = None


    def __init__(self,nameGiven, breedGiven):
        print("Param C")
        self.name = nameGiven
        self.breed = breedGiven

    def bark(self):
        print("Barking! -> ",self.name)


    def talk(self):
        print("talking")

chow = Dog("chow","mastiff")
chow.bark()

desi = Dog("rancho","desi")
desi.bark()

# More complex: default argument values so the no-argument call works too,
# and an optional attribute set after construction.
class Dog2:
    def __init__(self, name="unknown", breed="mixed", age=1):
        self.name = name
        self.breed = breed
        self.age = age
        self.tricks = []          # per-object list, not shared

    def learn(self, trick):
        self.tricks.append(trick)
        return self

    def profile(self):
        tricks = ", ".join(self.tricks) if self.tricks else "none"
        return f"{self.name} ({self.breed}, {self.age}y) knows: {tricks}"

    def __repr__(self):
        return f"Dog2({self.name!r})"


stray = Dog2()                       # all defaults
print(stray.profile())
print(Dog2("rex", "lab", 3).learn("sit").learn("roll").profile())

# This will not call the Default PARAM, we don't have defalt c
try:
    straydog = Dog()
except TypeError as error:
    print("TypeError:", error)
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

# This will not call the Default PARAM, we don't have defalt c
straydog = Dog()
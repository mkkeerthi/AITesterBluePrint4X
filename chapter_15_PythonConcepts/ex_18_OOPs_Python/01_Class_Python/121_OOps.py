# 121_OOps.py
# First OOP example: defines a Person class with class attributes (name, id, age...)
# and behaviours (methods that take self as the first parameter). Three Person
# objects are created, but none of the methods are called.
class Person:
    # Attributes
    name = None
    id = None
    age = None
    email = None
    height = None
    gender = None
    phone_no = None
    address = None


    # Behavriour
    def talk(self):  # self - this , self will be first argument in every behaviour.
        print("I can Talk")

    def sleep(self, name):  # Arg with No Return
        print("I am a Method!!")
        print("Sleep", name)

    def sleep2(self, name):  # Arg with Return
        print("I am a Method!!")
        return None

    def walk(self):
        print("I am walking")

    def method_walk_return(self):  # No Arg with Return
        return "I am walking"



def function_outside():
    print("Outside")


geeta = Person()
amit = Person()
navita = Person()

# More complex: actually use the objects - set attributes per instance and
# call the behaviours, including a method that returns a value.
geeta.name = "Geeta"
geeta.age = 30
geeta.talk()
geeta.sleep("Geeta")

amit.name = "Amit"
amit.walk()
print(amit.method_walk_return())

# Each object keeps its own state - changing one does not affect the others.
print("geeta:", geeta.name, "| amit:", amit.name)
print("navita untouched:", navita.name)

# Class attributes describe the shape; instance attributes hold the data.
print("class default:", Person.name)
print("instance value:", geeta.name)

# Calling a method directly through the class passes self explicitly.
Person.talk(geeta)

# Type checks confirm these are Person instances.
print(isinstance(geeta, Person), type(amit).__name__)

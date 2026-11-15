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

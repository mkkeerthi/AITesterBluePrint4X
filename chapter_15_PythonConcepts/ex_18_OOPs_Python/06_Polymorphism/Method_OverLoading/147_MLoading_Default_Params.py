# 147_MLoading_Default_Params.py
# Simulates overloading with default parameters: say_name() is defined twice but
# only the second version (name, lastname="Dutta") survives, so one call may omit lastname.
class Person:
    def say_name(self, name):
        print("Hi", name)

    def say_name(self, name, lastname="Dutta"):
        print("Hi,", name, lastname)


t = Person()
t.say_name("Dutta")

t = Person()
t.say_name("Pramod", "Sharma")
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

# More complex: keyword arguments make the "optional" parameter clearer, and
# you can see which definition actually survived by inspecting the signature.
import inspect

print("signature:", inspect.signature(Person.say_name))
p = Person()
p.say_name(name="Pramod")
p.say_name(name="Pramod", lastname="Kumar")


# Overload-style variants with a *separator and keyword-only arguments.
class Greeter:
    def greet(self, name, *, formal=False):
        if formal:
            print(f"Good morning, {name}.")
        else:
            print(f"Hi {name}!")


g = Greeter()
g.greet("Amit")
g.greet("Amit", formal=True)

# The single definition is easy to extend without breaking existing calls.
class Greeter2:
    def greet(self, name, greeting="Hi", punctuation="!"):
        print(f"{greeting}, {name}{punctuation}")


g2 = Greeter2()
g2.greet("Navita")
g2.greet("Navita", "Hello", ".")
g2.greet("Navita", punctuation="?")
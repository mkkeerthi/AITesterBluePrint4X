# 137_REAL.py
# Access-modifier demo with a family analogy: public_var, _protected_var and
# __private_var. Note that mom() and __wife() are defined inside __init__, so
# they are locals rather than methods; the commented calls fail (name mangling).
class Home:
      def __init__(self):
        self.public_var = "father"
        self._protected_var = "brother"
        self.__private_var= "baby"

        def mom(self):
            print(self.__private_var)
            self.__wife()

        def __wife(self):
            print("Private Wife")


object_ref = Home()
# object_ref.__wife()
# object_ref.__private_var

# More complex: the version where mom() and __wife() are real METHODS, so
# they can be called through the class, plus the mangled-name check.
class Home2:
    def __init__(self):
        self.public_var = "father"
        self._protected_var = "brother"
        self.__private_var = "baby"

    def mom(self):
        print("from mom:", self.__private_var)
        self.__wife()

    def __wife(self):
        print("Private Wife")


house = Home2()
print(house.public_var)
print(house._protected_var)

house.mom()

# The commented calls in the original would raise AttributeError; shown here
# inside try/except so the file keeps running.
try:
    house.__wife()
except AttributeError as error:
    print("AttributeError:", error)

# Name mangling turns __wife into _Home2__wife.
house._Home2__wife()
print("private value via mangled name:", house._Home2__private_var)
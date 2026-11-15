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
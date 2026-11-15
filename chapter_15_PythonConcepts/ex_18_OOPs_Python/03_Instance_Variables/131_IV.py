# 131_IV.py
# Contrasts variable kinds: g is global, i is a class/instance attribute, and l
# is local to print_infor(). Reading self.l raises AttributeError because l was
# never stored on the object; talk() can read both self.i and the global g.
g = 10 # Global

class Person:
    i = 11 # Instance, Class , Attribute...property
    def print_infor(self):
        l = 10 # local l varaible
        print(self.l)

    def talk(self):
        print(self.i)
        print(g)
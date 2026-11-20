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

# More complex: the same three scope kinds exercised properly, plus the
# classic "class attribute shared / instance attribute per object" distinction.
counter = 0


class Counter:
    shared = 0                       # class attribute

    def __init__(self, name):
        self.name = name             # instance attribute
        self.local_calls = 0

    def bump(self):
        Counter.shared += 1          # modifies the class attribute
        self.local_calls += 1        # modifies this object's attribute
        global counter
        counter += 1                 # modifies the module-level variable
        return f"{self.name}: shared={Counter.shared}, own={self.local_calls}, global={counter}"


c1 = Counter("one")
c2 = Counter("two")
print(c1.bump())
print(c2.bump())
print(c1.bump())
print("instances:", c1.__dict__, c2.__dict__)
print("class attribute:", Counter.shared)

# This is the AttributeError the original print_infor() would raise.
p = Person()
try:
    p.print_infor()
except AttributeError as error:
    print("AttributeError:", error)

# Values set on an instance stay on that instance.
p.i = 99
p.talk()
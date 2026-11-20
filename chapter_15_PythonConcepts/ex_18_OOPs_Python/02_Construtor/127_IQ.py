# 127_IQ.py
# Interview-style constructor question: each object gets its own name from the
# constructor argument, so calling printName() shows independent values ("bobby"
# vs "ruks") rather than sharing one class-level value.
class Dog:
    name = None
    breed = None
    def __init__(self,nameGiven):
        self.name = nameGiven
    def printName(self):
        print(self.name)

chow_ref = Dog("bobby")
mow_ref = Dog("ruks")

chow_ref.printName()
mow_ref.printName()

# More complex: prove the values live on the instances (obj.__dict__), that
# the class attribute is only a fallback, and that copying is shallow.
print(chow_ref.__dict__, mow_ref.__dict__)
print("class attribute:", Dog.name)          # still None

Dog.name = "class-level"
fresh = Dog("still-per-object")
print("instance wins:", fresh.name)
print("class attribute:", Dog.name)

# Setting on the class does not change existing instances that have their own.
print(chow_ref.name, "|", fresh.name)

# Two names, one object - copying a reference, not the data.
alias = chow_ref
alias.name = "renamed"
print(chow_ref.name)                         # changed through the alias

# id() shows both names point at the same object.
print(id(chow_ref) == id(alias))
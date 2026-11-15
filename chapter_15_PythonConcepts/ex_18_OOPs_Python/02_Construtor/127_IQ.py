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
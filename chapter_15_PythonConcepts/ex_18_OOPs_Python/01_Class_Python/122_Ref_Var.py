# 122_Ref_Var.py
# A Dog class with attributes and methods. Shows that a method uses self to
# reach the object's own data (self.name), and that Dog() creates an object
# stored in the reference variable chow.
class Dog:
    # A
    name = None
    breed = None
    height = None
    weight = None
    # B
    def bark(self):
        print("Barking")
        # print(name)
        print(self.name)

    def talk(self):
        print("Talking")


chow = Dog()

# Dog() - Object
# chow -> Object Ref

# More complex: several objects from one class, each with its own state,
# plus a class-level counter and a method that returns a value.
class Account:
    total_accounts = 0          # class attribute, shared by all objects

    def __init__(self, owner, balance=0):
        self.owner = owner      # instance attributes, one per object
        self.balance = balance
        Account.total_accounts += 1

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def describe(self):
        return f"{self.owner}: {self.balance}"

    def __repr__(self):
        return f"Account({self.owner!r}, {self.balance})"


a1 = Account("Pramod", 100)
a2 = Account("Amit")
print(a1.deposit(50), a2.deposit(20))
print(a1.describe(), "|", a2.describe())
print("accounts created:", Account.total_accounts)
print([a1, a2])

# Objects compared by identity, not by value, unless __eq__ is defined.
print("same object?", a1 is a2, "| equal values?", a1.describe() == a2.describe())
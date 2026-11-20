# 141_MI_002.py
# Interview question on method resolution order (MRO): both parents define
# money(), and Child(Father2, Father1) picks Father2.money() because the
# left-most parent wins the lookup.
class Father1:
    def money(self):
        print("F1 Money")


class Father2:
    def money(self):
        print("F2 Money")

# MRO method resolution order
class Child(Father2,Father1 ):
    def give_money(self):
        print("Son")
        self.money()


c = Child()
c.give_money()

# More complex: inspect the MRO directly, and see how the order changes the
# winner. This is the exact interview follow-up.
print("MRO of Child:", [cls.__name__ for cls in Child.__mro__])


class Child2(Father1, Father2):     # reversed parent order
    def give_money(self):
        self.money()


Child2().give_money()               # now F1 Money wins

# Rules to remember:
# 1. The order you list the parents in decides.
# 2. The first parent found in the MRO wins.
# 3. Call super().method() in a parent if you want cooperative chaining.

class Mixed(Father1, Father2):
    def money(self):
        # Reuse both parents explicitly when you need all versions.
        Father1.money(self)
        Father2.money(self)
        print("Mixed total")


Mixed().money()

# A parent that does not define money() - Python keeps searching along the
# MRO and finds the next parent that does.
class EmptyParent:
    pass


class FromSecondParent(EmptyParent, Father2):
    pass


print("falls through to Father2:", end=" ")
FromSecondParent().money()
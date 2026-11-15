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
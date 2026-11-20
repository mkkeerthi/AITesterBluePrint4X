# 130_REAL.py
# Small real-world style class: Baby stores the name passed to its constructor
# and printName() displays it; two babies keep separate values.
class Baby:
    name : None

    def __init__(self, nameGiven):
        self.name = nameGiven

    def printName(self):
        print(self.name)


b = Baby("gugu")
b2 = Baby("sema")
b.printName()
b2.printName()

# More complex: a Baby class with a default age, a class-level counter and
# dunder methods so objects print and compare sensibly.
class Baby2:
    count = 0

    def __init__(self, name, age_months=0):
        self.name = name
        self.age_months = age_months
        Baby2.count += 1

    def __str__(self):
        return f"{self.name} ({self.age_months} months)"

    def __eq__(self, other):
        return isinstance(other, Baby2) and self.name == other.name

    def __lt__(self, other):
        return self.age_months < other.age_months

    def older_than(self, other):
        return self.age_months > other.age_months


a = Baby2("gugu", 6)
c = Baby2("sema", 9)
print(a, "|", c)
print("older:", c.older_than(a), "| same name:", a == Baby2("gugu"))
print("sorted:", [str(x) for x in sorted([c, a])])
print("babies created:", Baby2.count)
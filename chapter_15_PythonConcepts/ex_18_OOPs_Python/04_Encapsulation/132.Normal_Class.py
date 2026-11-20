# 132.Normal_Class.py
# Baseline "no encapsulation" class: Car stores name, make and model from its
# constructor and start_engine() prints them. Two Car objects are created.
class Car:
    name: None
    make: None
    model: None
    
    def __init__(self, o_name, o_make, o_model):
        self.name = o_name
        self.make = o_make
        self.model = o_model

    def start_engine(self):
        print("Starting a car with the name " + self.name)
        print("Starting a car with the make " + self.make)
        print("Starting a car with the model " + self.model)



lambo = Car("Lambo", "V6", "2023")
lambo.start_engine()

mg_hector = Car("Hector","1.5+ Turbo","2024")
mg_hector.start_engine()

# More complex: because nothing is protected, any attribute can be changed
# from outside - which is exactly what encapsulation prevents.
lambo.model = "1999"
lambo.name = "Renamed"
print("changed freely:", lambo.name, lambo.model)

lambo.unknown_attribute = "anything goes"
print("dynamic attribute added:", lambo.__dict__)

# A cleaner variant: validate in the constructor and expose a single
# describe() method instead of scattering attribute reads everywhere.
class Car2:
    def __init__(self, name, make, model, year=None):
        if not name or not make:
            raise ValueError("name and make are required")
        self.name = name.strip()
        self.make = make.strip()
        self.model = model.strip()
        self.year = year

    def describe(self):
        return f"{self.name} | {self.make} | {self.model}" + (f" | {self.year}" if self.year else "")

    def __str__(self):
        return self.describe()


print(Car2("Hector", "1.5+ Turbo", "2024", 2024))

try:
    Car2("", "V6", "2023")
except ValueError as error:
    print("ValueError:", error)
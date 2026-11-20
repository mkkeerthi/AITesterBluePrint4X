# 125_Default_Const.py
# Shows a default constructor: __init__(self) takes no extra arguments and is
# called automatically whenever a Dog object is created (it prints "Hi").
class Dog:
     # Attributes - Instance variables | Data variables
    name = None
    breed = None
    height = None
    weight = None
    race = None

    def __init__(self):  # Default C - No Parameter
        print("Hi")

# More complex: an object is created below (so the constructor actually runs),
# and a second class shows a default constructor that initialises real defaults.
tommy = Dog()

class Config:
    def __init__(self):
        self.timeout = 30
        self.retries = 3
        self.base_url = "https://api.example.com"

    def show(self):
        print(f"timeout={self.timeout}, retries={self.retries}, url={self.base_url}")


cfg = Config()
cfg.show()

# The class-level attributes above are shared; instance ones set in __init__
# are per object, so changing one object does not affect another.
tommy.name = "Tommy"
other = Dog()
other.name = "Bruno"
print(tommy.name, other.name)
print("class default still:", Dog.name)
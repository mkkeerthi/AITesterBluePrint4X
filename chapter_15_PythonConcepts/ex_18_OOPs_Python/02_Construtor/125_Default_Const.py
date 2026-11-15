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
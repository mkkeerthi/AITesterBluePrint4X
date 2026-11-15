# 123_Create_Class.py
# A minimal class with a class attribute (model) and a method. An object is
# created, its attribute is set, and the method is called. Note: talk() lacks
# self, so calling it raises a TypeError in Python 3.
class MobilePhone:
    model = None

    def talk():
        print("Hello")


ipone = MobilePhone()
ipone.model = "iphone 18 Pro Max"
ipone.talk()
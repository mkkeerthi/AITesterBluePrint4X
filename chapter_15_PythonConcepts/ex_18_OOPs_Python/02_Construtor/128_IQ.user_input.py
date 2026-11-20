# 128_IQ.user_input.py
# A Person class whose constructor asks the user for values (name, age, phone,
# occupation) at object-creation time; display_values() then prints them back.
class Person:
    name = None
    age = None
    phone = None
    occupation = None

    def __init__(self):
        print("Let's take the user input, Please share the name,age,phone,occ")
        self.name = input("Enter the name\n")
        self.age = input("Enter the age\n")
        self.phone = input("Enter the Phone\n")
        self.occupation = input("Enter the occupation\n")

    def display_values(self):
        print("Name is ", self.name, "Age is ", self.age, "Phone is", self.phone, "occupation", self.occupation)

amit = Person()
amit.display_values()

# More complex: collect the same details through the constructor with
# validation and defaults, so objects can also be built without prompting.
class Person2:
    def __init__(self, name, age=0, phone="n/a", occupation="unknown"):
        self.name = name.strip() or "anonymous"
        self.age = int(age)
        self.phone = phone
        self.occupation = occupation

    @classmethod
    def from_input(cls):
        # Reads interactively; commented out so this file runs unattended.
        # return cls(input("Name: "), input("Age: "), input("Phone: "), input("Occupation: "))
        return cls("Pramod", "30", "9999999999", "SDET")

    def __str__(self):
        return f"{self.name}, {self.age}, {self.phone}, {self.occupation}"


p = Person2.from_input()
print(p)

# Validation happens in the constructor, so bad data fails immediately.
try:
    Person2("Amit", "not-a-number")
except ValueError as error:
    print("ValueError:", error)

print(Person2("   "))   # blank name falls back to "anonymous"
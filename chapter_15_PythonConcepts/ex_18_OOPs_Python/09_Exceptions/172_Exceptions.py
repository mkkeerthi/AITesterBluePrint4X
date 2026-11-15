# 172_Exceptions.py
# Defines a custom exception by subclassing Exception (InvalidAgeException) and
# raises it from can_you_drink() when the age is under 18.
# Create a Class for the Custom Exception

class InvalidAgeException(Exception):
    pass

def can_you_drink(age):
    if age < 18:
        raise InvalidAgeException("You can't drink!")
    else:
        print("You can drink!")

# can_you_drink(17)
can_you_drink(25)
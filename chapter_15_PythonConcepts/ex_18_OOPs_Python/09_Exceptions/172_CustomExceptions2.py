# 172_CustomExceptions2.py
# Defines a custom exception by subclassing Exception (InvalidAgeException) and
# raises it from can_you_drink() when the age is under 18.
# Create a Class for the Custom Exception

class InvalidAgeExceptionBasic(Exception):
    pass

def can_you_drink(age):
    if age < 18:
        raise InvalidAgeExceptionBasic("You can't drink!")
    else:
        print("You can drink!")

# can_you_drink(17)
can_you_drink(25)

# More complex: a custom exception with its own attributes, a helpful message
# and a handler that reads them back.
class InvalidAgeException(Exception):
    def __init__(self, age, message="age must be at least 18"):
        super().__init__(f"{message} (got {age})")
        self.age = age


class InvalidRangeError(InvalidAgeException):
    """A narrower error that also counts as an InvalidAgeException."""


def can_you_drink2(age):
    if not isinstance(age, int):
        raise TypeError("age must be an int")
    if age < 0 or age > 120:
        raise InvalidRangeError(age, "age is out of range")
    if age < 18:
        raise InvalidAgeException(age)
    return "You can drink!"


for candidate in [25, 17, 200, "18"]:
    try:
        print(candidate, "->", can_you_drink2(candidate))
    except InvalidRangeError as error:
        print(candidate, "-> range error:", error, "| age:", error.age)
    except InvalidAgeException as error:
        print(candidate, "-> too young:", error)
    except TypeError as error:
        print(candidate, "-> TypeError:", error)

# Because InvalidRangeError subclasses InvalidAgeException, catching the
# parent still catches the child - a key reason to build a hierarchy.
try:
    can_you_drink2(300)
except InvalidAgeException as error:
    print("caught by the parent handler:", type(error).__name__)
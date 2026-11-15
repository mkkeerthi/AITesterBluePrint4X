# 84_Deco_Imp.py
# Demonstrates a decorator with a driving analogy: add_security() wraps another
# function in a wrapper() that runs code before and after it, and is applied
# with @add_security to drive_ola_scooter().
def add_security(func):
    def wrapper():
        print("1.Before the function is called.")
        print("2.Add Helmet, Dashcash, gloves, knee guards, License")
        func()
        print("3.After the function is called.")
        print("4.Secure Driving, Leave all the items")

    return wrapper


@add_security
def drive_ola_scooter():
    print("I am driving ola scooter")


drive_ola_scooter()

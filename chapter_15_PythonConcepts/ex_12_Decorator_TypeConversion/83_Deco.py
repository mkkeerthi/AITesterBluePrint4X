# 83_Deco.py
# Warm-up for the decorator topic: a plain function sayGreeting() is defined
# and called. No decorator is used yet.
def sayGreeting():
    print("Hi")


sayGreeting()

# More complex: functions are objects, so they can be stored, passed and
# returned - which is exactly what makes decorators possible.
def say_bye():
    print("Bye")


# Store functions in a list and call them in a loop.
actions = [sayGreeting, say_bye]
for action in actions:
    action()

# Pass a function as an argument to another function.
def run_twice(fn):
    fn()
    fn()


run_twice(sayGreeting)

# A function can build and return another function.
def make_printer(prefix):
    def printer(message):
        print(prefix, message)
    return printer


error = make_printer("[ERROR]")
error("something failed")
print(type(error).__name__)

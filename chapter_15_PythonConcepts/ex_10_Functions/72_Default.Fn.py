# 72_Default.Fn.py
# Demonstrates a default parameter value: if no argument is given, name
# defaults to "QA"; otherwise the supplied value is used.
def greet_with_default_param(name="QA"):
    print("Hi,", name)


greet_with_default_param("Pramod")
greet_with_default_param("Amit")
greet_with_default_param()

# More complex: defaults for several parameters, mixing positional and
# keyword calls. Note the mutable-default pitfall below.
def create_user(name, role="tester", active=True):
    return {"name": name, "role": role, "active": active}


print(create_user("Pramod"))
print(create_user("Amit", role="admin"))
print(create_user("Navita", active=False))

# Pitfall: never use a mutable object (like []) as a default. The list is
# created once and shared between calls, so items pile up.
def add_item_bad(item, bucket=[]):
    bucket.append(item)
    return bucket


print(add_item_bad("a"))
print(add_item_bad("b"))   # ['a', 'b'] - same list reused!


# Fix: default to None and create a fresh list inside the function.
def add_item_good(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


print(add_item_good("a"))
print(add_item_good("b"))  # ['b'] - independent lists
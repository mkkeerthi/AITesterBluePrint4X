# 74_Fn_Keyword_Arg.py
# Shows keyword arguments: callers pass values by parameter name, so the
# order of arguments does not matter. Also introduces f-strings for formatting.
def display_information(name, role):
    print(f"Name : {name}, role is {role}")

# Call you can mention the keyword.
display_information(name="Pramod2", role="QA2")
display_information(role="QA3", name="Pramod3")

# More complex: mixing positional and keyword arguments, and forwarding a
# dict of options with ** (kwargs unpacking) into keyword parameters.
def create_test(name, priority="P2", owner="QA"):
    print(f"{name} [{priority}] owner={owner}")


create_test("login")                                   # defaults
create_test("login", "P0")                             # positional
create_test("login", priority="P1", owner="Pramod")    # keywords

options = {"priority": "P0", "owner": "Amit"}
create_test("checkout", **options)                     # unpack a dict

# Positional arguments must come before keyword arguments in a call.
# create_test(priority="P1", "login")  -> SyntaxError
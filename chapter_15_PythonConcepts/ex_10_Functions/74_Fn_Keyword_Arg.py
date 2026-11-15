# 74_Fn_Keyword_Arg.py
# Shows keyword arguments: callers pass values by parameter name, so the
# order of arguments does not matter. Also introduces f-strings for formatting.
def display_information(name, role):
    print(f"Name : {name}, role is {role}")

# Call you can mention the keyword.
display_information(name="Pramod2", role="QA2")
display_information(role="QA3", name="Pramod3")
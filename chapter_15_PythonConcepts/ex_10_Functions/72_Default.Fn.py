# 72_Default.Fn.py
# Demonstrates a default parameter value: if no argument is given, name
# defaults to "QA"; otherwise the supplied value is used.
def greet_with_default_param(name="QA"):
    print("Hi,", name)


greet_with_default_param("Pramod")
greet_with_default_param("Amit")
greet_with_default_param()
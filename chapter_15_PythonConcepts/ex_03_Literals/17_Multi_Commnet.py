# 17_Multi_Commnet.py
# Demonstrates comments: single-line comments with '#', and a triple-quoted
# block used as a multi-line comment (its contents are not executed).
# This is comment

"""
This is Multiple Line Comment
Here the code you write will not be executed
Why this is Used?
age = 65
print(type(age))

"""

# This is single comment
print("Hi")

# More complex: a docstring-style block at the top of a function documents it.
def calculate_discount(price, percent):
    """Return the price after applying a percentage discount.

    Args:
        price: original price
        percent: discount percentage (e.g. 10 for 10%)
    """
    discount = price * percent / 100
    return price - discount


# The function docstring is available at runtime through __doc__.
print(calculate_discount(200, 10))
print(calculate_discount.__doc__)

"""
A triple-quoted block used like this is just a string literal:
Python evaluates it and throws it away, so it acts as a comment block.
It is handy for longer explanations, notes or disabled code.
"""
print("Done")
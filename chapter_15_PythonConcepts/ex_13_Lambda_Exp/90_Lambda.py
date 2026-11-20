# 90_Lambda.py
# Compares a normal def function with an equivalent lambda: both triple a
# number, but the lambda is written in a single short expression.
def triple_number(num):
    return num*3

print(triple_number(3))

result = lambda num: num*3
print(result(3))

# More complex: lambdas shine where a tiny function is used once - as a key,
# a default factory, or an argument to sorted/map/filter.
numbers = [5, 2, 9, 1]
print(sorted(numbers, key=lambda n: -n))     # descending
print(max(numbers, key=lambda n: abs(n - 5)))  # farthest from 5

people = [("pramod", 30), ("amit", 25), ("navita", 35)]
people.sort(key=lambda person: person[1])
print(people)

# A lambda can have a default argument and *args, but only ONE expression.
greet = lambda name, greeting="Hi": f"{greeting} {name}"
print(greet("Pramod"))
print(greet("Amit", "Hello"))

# The body is an expression, so no statements (no assignment, no print loop).
square_all = lambda values: [v * v for v in values]
print(square_all([1, 2, 3]))
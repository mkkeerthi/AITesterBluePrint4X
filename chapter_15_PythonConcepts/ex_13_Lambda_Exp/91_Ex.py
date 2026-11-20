# 91_Ex.py
# Rewrites two ordinary functions as lambdas: one multiplying two numbers and
# one summing three numbers, then calls each lambda.
def mul(a, b):
    return a * b

mul_l = lambda a, b: a * b
print(mul_l(3, 4))

def sum_three_num(a, b, c):
    return a + b + c


op_f = lambda a, b, c: a + b + c
print(op_f(3, 4, 5))

# More complex: lambdas with a condition (ternary) and as sort/filter keys.
max_of_two = lambda a, b: a if a > b else b
print(max_of_two(10, 7))

is_even = lambda n: n % 2 == 0
print(is_even(10), is_even(7))

# The classic functional trio: map, filter and reduce with lambdas.
numbers = [1, 2, 3, 4, 5]
print(list(map(lambda n: n ** 2, numbers)))
print(list(filter(lambda n: n % 2 == 0, numbers)))

from functools import reduce
print(reduce(lambda acc, n: acc + n, numbers))

# Lambdas assigned to names work, but PEP 8 prefers def for anything reused.
distance = lambda x1, y1, x2, y2: ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
print(round(distance(0, 0, 3, 4), 2))
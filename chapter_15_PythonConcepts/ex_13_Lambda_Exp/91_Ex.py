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
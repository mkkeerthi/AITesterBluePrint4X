# 90_Lambda.py
# Compares a normal def function with an equivalent lambda: both triple a
# number, but the lambda is written in a single short expression.
def triple_number(num):
    return num*3

print(triple_number(3))

result = lambda num: num*3
print(result(3))
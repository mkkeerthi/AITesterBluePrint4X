# 73_Fn_Mul_Returb.py
# Shows a function returning multiple values at once (as a tuple), which the
# caller unpacks into three separate variables.
def math_operations(a, b):
    return a + b, a - b, a * b


sum_result, diff_result, mul_result = math_operations(3, 4)
print(sum_result)
print(diff_result)
print(mul_result)
# 73_Fn_Mul_Returb.py
# Shows a function returning multiple values at once (as a tuple), which the
# caller unpacks into three separate variables.
def math_operations(a, b):
    return a + b, a - b, a * b


sum_result, diff_result, mul_result = math_operations(3, 4)
print(sum_result)
print(diff_result)
print(mul_result)

# More complex: return more results including division, handle zero, and
# also show that the returned value is a single tuple.
def full_math(a, b):
    quotient = a / b if b else None
    return a + b, a - b, a * b, quotient


results = full_math(10, 2)
print(results, type(results))

# Unpack all four, ignoring the ones you don't need with _.
total, _, product, quotient = full_math(10, 2)
print(total, product, quotient)

# A realistic use: return a pass/fail outcome and a message together.
def check_status(code):
    if 200 <= code < 300:
        return True, "ok"
    return False, f"unexpected status {code}"


passed, message = check_status(201)
print(passed, message)
passed, message = check_status(500)
print(passed, message)
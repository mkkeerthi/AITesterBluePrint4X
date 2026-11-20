# 77_IQ.py
# Works through default arguments combined with positional and keyword
# arguments, showing which values the defaults supply.
def sum_three(a=1, b=1, c=1):
    return a + b + c


result1 = sum_three()
print(result1)

result2 = sum_three(1, 2)
print(result2)

result3 = sum_three(1, 2, 3)
print(result3)

result5 = sum_three(b=67, a=10, c=45)
print(result5)

result6 = sum_three(a=10, b=67, c=45)
print(result6)

# More complex: what breaks when defaults and required parameters are mixed,
# and how keyword-only arguments change the rules.
def mixed(required, optional=10):
    return required + optional


print(mixed(5))              # 15
print(mixed(5, 20))          # 25
print(mixed(optional=1, required=2))  # order-free with keywords

# A required parameter cannot follow a defaulted one without making it
# keyword-only: def bad(a=1, b) is a SyntaxError.

# Keyword-only parameters (after *) must be passed by name.
def keyword_only(a, *, b=1, c=2):
    return a + b + c


print(keyword_only(10))
print(keyword_only(10, b=5))
# keyword_only(10, 5)  -> TypeError: takes 1 positional argument

# A subtle order-of-evaluation case: defaults are evaluated once, at
# definition time, so mutable defaults are shared.
def collect(item, store=[]):
    store.append(item)
    return list(store)


print(collect("a"))
print(collect("b"))
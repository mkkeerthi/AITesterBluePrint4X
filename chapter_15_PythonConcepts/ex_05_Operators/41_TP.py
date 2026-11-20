# 41_TP.py
# Demonstrates the ternary (conditional) expression: value_if_true if condition
# else value_if_false, with the equivalent if/else version shown commented out.
# Ternary Operator:  if-else statement.
x = 10
y = 20

print("x is greater than y" if x > y else "x is less than y")

# if x > y:
#     print("x is grater")
# else:
#     print("y is greater")

# More complex: the ternary expression returns a value, so it can be
# assigned, chained, or used inside a format string.
status = 200
label = "OK" if status == 200 else "ERROR"
print(label)

score = 78
grade = "A" if score >= 90 else "B" if score >= 75 else "C"
print(f"Score {score} -> grade {grade}")

# Ternary inside a function call and inside a comprehension.
print("Even" if 10 % 2 == 0 else "Odd")
parity = ["even" if n % 2 == 0 else "odd" for n in range(1, 6)]
print(parity)

# A default value chosen conditionally, useful when parsing config.
timeout = None
effective_timeout = timeout if timeout is not None else 30
print(effective_timeout)
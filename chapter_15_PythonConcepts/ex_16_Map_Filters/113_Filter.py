# 113_Filter.py
# Introduces filter(): keeps only the elements for which a function returns
# True, here selecting the even numbers from a list.
nums = [1, 2, 3, 4, 5, 6]


def even_num(x):
    return x%2==0

print(list(filter(even_num, nums)))

# More complex: filter with None (keeps truthy values), combining filters,
# and comparing with a comprehension which is often more readable.
values = [0, 1, "", "text", None, [], [1], False, True]
print("truthy only:", list(filter(None, values)))

print("positive and even:", list(filter(lambda n: n > 0 and n % 2 == 0, [-2, -1, 0, 2, 3, 4])))

# filter() returns an iterator, so wrap it in list() to reuse or print it.
odds = filter(lambda n: n % 2 != 0, nums)
print("odds:", list(odds))
print("iterator used up:", list(odds))

# The equivalent comprehension.
print("comprehension:", [n for n in nums if n % 2 == 0])

# Realistic: keep only valid email addresses from a messy list.
emails = ["a@x.com", "not-an-email", "b@y.com", "", "c@z.com"]
valid = list(filter(lambda e: "@" in e and "." in e.split("@")[-1], emails))
print("valid emails:", valid)

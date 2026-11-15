# 113_Filter.py
# Introduces filter(): keeps only the elements for which a function returns
# True, here selecting the even numbers from a list.
nums = [1, 2, 3, 4, 5, 6]


def even_num(x):
    return x%2==0

print(list(filter(even_num, nums)))

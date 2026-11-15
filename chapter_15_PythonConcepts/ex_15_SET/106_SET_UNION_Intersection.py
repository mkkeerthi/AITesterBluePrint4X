# 106_SET_UNION_Intersection.py
# Set algebra between {1,2,3} and {3,4,5}: union (|), intersection (&) and
# difference (-), each written with operators and their named method equivalents.
a = {1, 2, 3}
b = {3, 4, 5}

print(a | b)
print(a.union(b))

print(a & b)            # {3}
print(a.intersection(b))


print(a - b)
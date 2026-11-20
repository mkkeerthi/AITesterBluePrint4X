# 93_List.py
# Introduces lists: ordered, mutable collections written in square brackets.
# Creates a homogeneous and a mixed-type list, then checks type, length and indexing.
# List - Collection  of items
# grocery List - butter, bread, banana, paneer.
# 10th marks - 90,91,92, 78, 56

my_list = [1, 2, 3]  # Same type of data (int)
my_list2 = [1, True, "Pramod", 12.34]

print(my_list)
print(type(my_list)) # <class 'list'> , []
print(len(my_list))
print(my_list[0])
print(my_list[2])
# print(my_list[6]) # IndexError: list index out of range

# More complex: negative indexing, slicing and membership checks.
grades = [90, 91, 92, 78, 56, 88]
print("Last:", grades[-1])            # last item
print("First two:", grades[:2])       # slice
print("Every other:", grades[::2])    # step
print("Reversed:", grades[::-1])
print("Top 3:", sorted(grades, reverse=True)[:3])
print("Contains 78:", 78 in grades)
print("Index of 78:", grades.index(78))

# Lists can grow and shrink; the original object stays the same.
grades.append(100)
grades.remove(56)
print("Updated:", grades, "length:", len(grades))

# A list of lists behaves like a small table.
table = [[1, 2, 3], [4, 5, 6]]
for row in table:
    print(row, "sum:", sum(row))
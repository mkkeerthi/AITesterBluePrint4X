# 95_List_All_Fn.py
# Tour of common list methods: indexing, append(), extend(), insert(), remove()
# and copy(), showing that a copied list is independent of the original.
my_list = [1, 2, 3]
# Indexing
print("element at the index 0 - ", my_list[0])
print("element at the index 1 - ", my_list[1])
print("element at the index 2 - ", my_list[2])

my_list.append(4)
print(my_list)


my_list.append(5)
print(my_list)


# extend() - Append a new list
my_list.extend([7, 8, 10, 9])
print(my_list)


# insert()
my_list.insert(1,"Dutta")
print(my_list)
print(len(my_list))

my_list.insert(0, 0)
print(my_list)

my_list[1] = "Amit"
print(my_list)

my_list.remove("Amit")
print(my_list)

my_copy_list = my_list.copy()
print(my_list)
print(my_copy_list)

my_copy_list.remove("Dutta")

print(my_list)
print(my_copy_list)

# More complex: the remaining list methods - sort, reverse, index, count -
# plus the difference between sort() (in place) and sorted() (new list).
scores = [88, 42, 91, 67, 42]
scores.sort()                 # in place, returns None
print("sorted in place:", scores)

descending = sorted(scores, reverse=True)   # new list
print("sorted() copy:", descending)
print("original unchanged by sorted():", scores)

print("count of 42:", scores.count(42))
print("index of 91:", scores.index(91))

scores.reverse()
print("reversed in place:", scores)

# Stack and queue patterns: append/pop on the right, insert(0)/pop(0) on the left.
stack = []
stack.append("a")
stack.append("b")
print("popped:", stack.pop(), "remaining:", stack)

# Joining list items into text, and splitting text back into a list.
words = ["run", "the", "tests"]
print("-".join(words).upper())
print("one,two,three".split(","))

# A nested list needs each row copied separately - [[0]*3]*2 shares rows.
grid_bad = [[0] * 3] * 2
grid_bad[0][0] = 1
print("shared rows:", grid_bad)

grid_ok = [[0] * 3 for _ in range(2)]
grid_ok[0][0] = 1
print("independent rows:", grid_ok)
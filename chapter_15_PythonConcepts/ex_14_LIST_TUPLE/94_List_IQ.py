# 94_List_IQ.py
# Shows that list elements can be changed by index (lists are mutable), how to
# iterate a list with for, and that range() produces a sequence of numbers.
my_list = [1, 2, 3]

my_list[0] = "Pramod"
my_list[1] = "Dutta"
my_list[1] = "Dutta"

print(my_list)

for element in my_list:
    print(element)


# range() this also return the list
for i in range(1, 5):  # 1,2,3,4
    print(i)

# More complex: mutation inside a loop, and the aliasing trap.
# Two names pointing at ONE list see each other's changes.
original = [1, 2, 3]
alias = original          # same object, not a copy
alias.append(4)
print("original:", original, "alias:", alias, "same object:", original is alias)

# A real copy is independent.
real_copy = original.copy()   # or list(original)
real_copy.append(99)
print("original still:", original)
print("copy:", real_copy)

# Modifying a list while iterating it gives surprising results - iterate a
# copy instead when removing items.
numbers = [1, 2, 3, 4, 5, 6]
for number in numbers.copy():
    if number % 2 == 0:
        numbers.remove(number)
print("odds only:", numbers)

# Building a new list is usually cleaner than mutating in place.
odds = [n for n in [1, 2, 3, 4, 5, 6] if n % 2 != 0]
print("via comprehension:", odds)
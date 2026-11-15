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
# 96_List_Ex.py
# Demonstrates removing items from a list: pop() removes and returns the last
# item (or an item at a given index), and clear() empties the list.
squares = [1, 4, 9, 16, 25]

print(squares)
print(squares.pop()) # Remove and return item at index (default last)

print(squares)
print(squares.pop(1))
print(squares)

squares.clear()
print(squares)

# More complex: use a list as a stack, then safely remove by value with
# a guard, and show del vs remove vs pop.
tasks = ["login", "search", "checkout"]
last = tasks.pop()            # pop by position (default: last)
print("took:", last, "left:", tasks)

del tasks[0]                  # delete by index, returns nothing
print("after del:", tasks)

# remove() raises ValueError when the value is absent, so check first.
if "checkout" in tasks:
    tasks.remove("checkout")
print("after guarded remove:", tasks)

# A realistic queue: process items until the list is empty.
queue = ["job-1", "job-2", "job-3"]
while queue:
    current = queue.pop(0)    # FIFO
    print("processing", current)
print("queue drained:", queue)

# Slicing can replace whole sections without touching the object identity.
numbers = [1, 2, 3, 4, 5]
numbers[1:4] = [20, 30]
print("after slice assignment:", numbers)
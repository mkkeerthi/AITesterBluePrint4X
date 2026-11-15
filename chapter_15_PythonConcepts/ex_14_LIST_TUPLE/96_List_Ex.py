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
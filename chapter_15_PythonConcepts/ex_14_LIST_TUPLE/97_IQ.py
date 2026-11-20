# 97_IQ.py
# List operations: index() finds the first position of a value, count() counts
# occurrences, matrix[1][2] accesses a nested list, and max/min/sum aggregate numbers.
numbers = [10, 20, 30, 20, 40]
print(numbers.index(20))
print(numbers.count(20))

# Nested Lists
matrix = [[1,2,3], [4,5,6], [7,8,9]]
print(matrix[1][2])

# max() / min() / sum() Works for numerical lists.
print(max(numbers))  # 40
print(min(numbers))  # 10
print(sum(numbers))  # 120

# More complex: aggregates that combine several operations, and a matrix
# transposed with zip(*matrix).
print("Average:", sum(numbers) / len(numbers))
print("Unique values:", sorted(set(numbers)))
print("Sorted desc:", sorted(numbers, reverse=True))
print("Largest two:", sorted(numbers)[-2:])

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print("Row sums:", [sum(row) for row in matrix])
print("Transposed:", [list(col) for col in zip(*matrix)])
print("Diagonal:", [matrix[i][i] for i in range(len(matrix))])
print("Flat:", [value for row in matrix for value in row])

# index() raises ValueError if the item is missing - guard it.
target = 25
if target in numbers:
    print(numbers.index(target))
else:
    print(f"{target} not present")


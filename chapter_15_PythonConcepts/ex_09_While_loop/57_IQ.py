# 57_IQ.py
# for loop over 0-9 with if/else inside: prints "Five" when i is 5,
# otherwise prints the number itself.
for i in range(0, 10):
    if i == 5:
        print("Five")
    else:
        print(i)

# More complex: map each number to a word, falling back to the number.
words = {0: "zero", 3: "three", 7: "seven"}
for i in range(0, 10):
    print(words.get(i, i))

# The same loop written as a comprehension and joined into one line.
labels = ["Five" if i == 5 else str(i) for i in range(10)]
print(", ".join(labels))
# 003_PrintCommand.py
# Shows how print() can take multiple arguments and how the optional
# sep (separator between values) and end (what is printed at the end) control output.
print("Hello", "World")
print("Hello", "World", "TheTestingAcademy", sep="*")
print("Hello", "World", "TheTestingAcademy", sep="__")


print("*", "*", sep="-", end="\t")
print("*", "*", sep="_")


# More complex: build a small aligned table using sep and end.
header = ("Name", "Score", "Status")
rows = [("Pramod", 91, "PASS"), ("Amit", 47, "FAIL"), ("Navita", 88, "PASS")]

print(" | ".join(header))
print("-" * 24)
for name, score, status in rows:
    # end="" keeps all three prints on the same line
    print(f"{name:<8}", end="")
    print(f"{score:<6}", end="")
    print(f"{status:>6}")

# end=" " lets a loop print on one line instead of one line per item
for number in range(1, 6):
    print(number * number, end=" ")
print()  # finally move to a new line

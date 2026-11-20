# 51_For_Variants.py
# for loop over range(3, 5): stop is exclusive, so it prints only 3 and 4.
for i in range(3, 5):
    print(i)

# More complex: the four common range() shapes side by side.
print("range(5)        ->", list(range(5)))          # 0..4
print("range(2, 6)     ->", list(range(2, 6)))       # 2..5
print("range(1, 10, 3) ->", list(range(1, 10, 3)))   # 1,4,7
print("range(5, 0, -1) ->", list(range(5, 0, -1)))   # 5,4,3,2,1

# Looping directly over an iterable needs no index at all.
for letter in "abc":
    print(letter)

# The for/else pattern: else runs when no break happened.
for n in [1, 3, 5]:
    if n % 2 == 0:
        print("found an even number")
        break
else:
    print("all numbers were odd")
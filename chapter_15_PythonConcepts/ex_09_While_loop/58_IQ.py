# 58_IQ.py
# Demonstrates break: the loop exits immediately when i reaches 3,
# so it prints only 1 and 2.
for i in range(1, 6):
    if i == 3:
        break
    print(i)

# More complex: break to stop searching as soon as a match is found.
targets = ["login", "checkout", "logout"]
wanted = "checkout"

for index, name in enumerate(targets):
    print(f"checking {name}")
    if name == wanted:
        print(f"found '{wanted}' at position {index}")
        break

# Without break, a loop can inspect every item; with else it reports a miss.
for name in targets:
    if name == "payment":
        print("found payment")
        break
else:
    print("payment is not in the list")

# break also works in while loops, letting the condition stay True forever.
while True:
    answer = "stop"
    if answer == "stop":
        print("leaving the loop")
        break

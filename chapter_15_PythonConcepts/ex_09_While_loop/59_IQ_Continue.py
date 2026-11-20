# 59_IQ_Continue.py
# Demonstrates continue: when i is 3 the rest of the iteration is skipped,
# so 3 is not printed (1, 2, 4, 5 are).
for i in range(1, 6):
    if i == 3:
        continue
    print(i)

# More complex: continue to skip invalid records but keep processing the rest.
records = ["ok:1", "bad", "ok:2", "skip", "ok:3"]
processed = []

for record in records:
    if not record.startswith("ok:"):
        continue  # skip malformed entries
    processed.append(int(record.split(":")[1]))

print("Processed values:", processed)
print("Skipped:", len(records) - len(processed))

# continue in a while loop: be careful to update the counter before it,
# otherwise the loop may run forever.
n = 0
while n < 6:
    n += 1
    if n % 2 == 0:
        continue
    print("odd:", n)
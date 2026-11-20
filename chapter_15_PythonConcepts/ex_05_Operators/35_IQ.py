# 35_IQ.py
# Contrasts floor division // (returns an int, drops the fraction) with
# true division / (returns a float).
print(5//2)
print(5/2)

# More complex: how // rounds with negatives, and using % to detect parity.
print(7 // 2)     # 3
print(-7 // 2)    # -4 (floor, not truncation)
print(-7 % 2)     # 1  (remainder keeps the sign of the divisor)
print(7.5 // 2)   # 3.0 (floor division on floats returns a float)

# Even/odd check with % is the classic use of the modulo operator.
for number in range(1, 6):
    kind = "even" if number % 2 == 0 else "odd"
    print(f"{number} is {kind}")

# A realistic paging calculation: 47 records, 10 per page.
records, page_size = 47, 10
full_pages = records // page_size
last_page = 1 if records % page_size else 0
print(f"Full pages: {full_pages}, extra page: {last_page}")
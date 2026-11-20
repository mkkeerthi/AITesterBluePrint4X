# 56_Whioe.py
# while loop that simulates running test cases, printing test ids 0 through 9.
test_id = 0
while test_id < 10:
    print("Running the testcase -> ",test_id)
    test_id = test_id + 1

# More complex: a retry loop that stops on success or when retries run out.
attempt = 1
max_attempts = 4
succeeded = False

while attempt <= max_attempts and not succeeded:
    print(f"Attempt {attempt}: calling the API")
    # Pretend the API succeeds on the third try.
    succeeded = attempt == 3
    attempt += 1

print("Succeeded" if succeeded else "Gave up", f"after {attempt - 1} attempt(s)")

# while/else: the else runs only when the loop ends without break.
i = 0
while i < 3:
    i += 1
else:
    print("while loop finished normally, i =", i)
# 87_Time_Log.py
# Two useful decorators: time_decorator measures how long a function runs using
# time.time(), and print_logs adds start/end log lines. Both are stacked on
# test_ui_1, while test_ui_2 runs undecorated for comparison.
import time
# https://www.epochconverter.com/
def time_decorator(func):
    def wrapper():
        start_time = time.time()
        print(start_time)
        func()
        end_time = time.time()
        print(end_time)
        print("Total Time Take by Func -> ", end_time - start_time)
    return wrapper

def print_logs(func):
    def wrapper():
        print("Start the logs")
        func()
        print("End of the log")
    return wrapper


@time_decorator
@print_logs
def test_ui_1():
    print("Add a function, time taken by this function 1")
    time.sleep(2)


def test_ui_2():
    print("Add a function, time taken by this function 2")
    time.sleep(5)

print(" -----  ")

#with decor
test_ui_1()

print(" -----  ")
# without the decor
test_ui_2()

# More complex: a timing decorator that forwards arguments and returns the
# result, so it can wrap functions with parameters (not just `def f()`).
def timed(func):
    def wrapper(*args, **kwargs):
        started = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - started
            print(f"{func.__name__} took {elapsed:.4f}s")
    return wrapper


@timed
def download(pages, delay=0.2):
    for page in range(1, pages + 1):
        time.sleep(delay)
    return pages


print("downloaded pages:", download(3))
print("downloaded pages:", download(pages=2, delay=0.1))

# Stacking order matters: decorators apply bottom-up, and run top-down.
@timed
@print_logs
def quick():
    print("quick task")


quick()
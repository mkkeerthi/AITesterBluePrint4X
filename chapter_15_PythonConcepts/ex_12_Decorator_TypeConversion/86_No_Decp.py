# 86_No_Decp.py
# The "before decorators" version: setup (start), the test (test_ui) and
# teardown (end) are called manually in sequence, which a decorator could automate.
def start():
    print("Before the running UI TC")
    print("Start the Browser ")

def end():
    print("End the running UI TC")
    print("Quit the Browser ")

def test_ui():
    print("I will Test the UI")


start()
test_ui()
end()

# More complex: the same setup/test/teardown flow made automatic with a
# decorator, then applied to multiple tests.
def with_browser(func):
    def wrapper(*args, **kwargs):
        print("Start the Browser")
        try:
            result = func(*args, **kwargs)
        finally:
            print("Quit the Browser")   # teardown always runs
        return result
    return wrapper


@with_browser
def test_home_page():
    print("I will test the home page")
    return "passed"


@with_browser
def test_checkout():
    print("I will test the checkout flow")
    return "failed"


print(test_home_page())
print(test_checkout())

# The try/finally guarantees teardown even when the test raises.
@with_browser
def test_that_raises():
    raise ValueError("boom")


try:
    test_that_raises()
except ValueError as error:
    print("caught:", error)
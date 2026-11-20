# 85_Dec_New.py
# A practical test-automation decorator: before_after_ui_test() prints a
# message before and after running a UI test function it decorates.
def before_after_ui_test(func):
    def wrapper():
          print("Before the TC code execute!")
          func()
          print("After the TC Done")
    return wrapper

# func == test_ui

@before_after_ui_test
def test_ui():
     print("Hi, I am testing a UI Test")

test_ui()

# More complex: a decorator that can be reused across several tests and that
# forwards arguments, which is how real pytest fixtures/marks work.
def step(func):
    def wrapper(*args, **kwargs):
        print(f"STEP: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


@step
def test_login(username):
    print(f"logging in as {username}")
    return True


@step
def test_search(term, limit=5):
    print(f"searching '{term}' (limit {limit})")
    return []


print(test_login("pramod"))
print(test_search("python", limit=3))

# Decorators are just syntax sugar: this is the same as above.
def test_logout():
    print("logging out")


test_logout = step(test_logout)
test_logout()
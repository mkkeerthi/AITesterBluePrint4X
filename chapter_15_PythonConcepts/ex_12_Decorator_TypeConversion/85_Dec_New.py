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
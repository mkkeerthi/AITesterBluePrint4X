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
# 151_MOverride.py
# Method overriding across a class hierarchy: BaseTest.run() is overridden by
# LoginTest and APITest. The current call uses BaseTest, so its version runs;
# uncomment the other objects to see the subclass versions.
class TestSuite:
    def info(self):
        print("Test suite information")

class BaseTest(TestSuite):
    def setup(self):
        print("Base setup")

    def run(self):
        print("Base test execution")

class LoginTest(BaseTest):
    def run(self):  # overriding
        print("Login test execution")

class APITest(BaseTest):
    def run(self):  # overriding
        print("API test execution")


# t = LoginTest()
# t = APITest()
t = BaseTest()
t.run()

# More complex: iterate over every subclass through one shared interface, and
# show an override that calls the parent with super() plus a helper hook.
class UITest(BaseTest):
    def run(self):
        super().run()
        print("  UI-specific steps")


for cls in (BaseTest, LoginTest, APITest, UITest):
    obj = cls()
    print(f"{cls.__name__}:", end=" ")
    obj.run()

# Every class still reaches the grandparent method it did not override.
BaseTest().info()

# Overriding is resolved per object at call time (dynamic dispatch).
def execute(test):
    test.run()


execute(LoginTest())
execute(APITest())

# The parent implementation is still reachable explicitly.
BaseTest.run(LoginTest())
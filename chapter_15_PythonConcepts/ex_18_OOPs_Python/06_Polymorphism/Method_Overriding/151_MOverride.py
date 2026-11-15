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
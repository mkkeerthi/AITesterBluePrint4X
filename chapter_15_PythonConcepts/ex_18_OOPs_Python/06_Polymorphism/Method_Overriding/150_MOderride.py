# 150_MOderride.py
# Method overriding: LoginTest redefines run() from BaseTest. Only one object is
# active at a time - BaseTest.run() is called now; switch to LoginTest() to see
# the overridden version.
class BaseTest:
    def run(self):
        print("Running the Base Test")

class LoginTest(BaseTest):
    def run(self):
        print("Runnning Login Test")


t = BaseTest()
# t = LoginTest()
t.run()
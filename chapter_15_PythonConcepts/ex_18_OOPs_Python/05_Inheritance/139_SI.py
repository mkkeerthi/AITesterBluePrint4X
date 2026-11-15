# 139_SI.py
# Single inheritance: LoginTest extends BaseTest, so it inherits setUp() (and
# the class attributes) and calls it from run(). Also shows a private class
# attribute (__driver2) that is not inherited under that name.
class BaseTest:
    driver = "chrome"
    __driver2 = "firefox"

    def setUp(self):
        print("Base is setup!")

# si -> classSon(classFather)
class LoginTest(BaseTest):
    def run(self):
        self.setUp()
        print("Running TC")


t = LoginTest()
t.run()
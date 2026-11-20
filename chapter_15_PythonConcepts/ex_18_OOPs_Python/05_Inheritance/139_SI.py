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

# More complex: overriding, super(), and isinstance/issubclass checks.
class BaseTest2:
    driver = "chrome"
    __driver2 = "firefox"          # not inherited under this name

    def setUp(self):
        print("Base is setup!")

    def log(self, message):
        print(f"[base] {message}")


class LoginTest2(BaseTest2):
    driver = "firefox"             # overrides the attribute for this class only

    def setUp(self):
        super().setUp()            # run the parent version first
        print("LoginTest extra setup")

    def log(self, message):
        super().log(message.upper())   # extend, don't replace

    def run(self):
        self.setUp()
        self.log("running login test")


t2 = LoginTest2()
t2.run()
print("own driver:", t2.driver, "| parent driver:", BaseTest2.driver)
print("isinstance:", isinstance(t2, BaseTest2), "issubclass:", issubclass(LoginTest2, BaseTest2))

# The private attribute is name-mangled into _BaseTest2__driver2, so it is
# still reachable - just not as a plain inherited name.
print("mangled parent attr:", t2._BaseTest2__driver2)
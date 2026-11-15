# 143_HI.py
# Hierarchical inheritance: two sibling classes (LoginTest, SignupTest) both
# inherit the same parent (BaseTest), so both get setup() from it.
class BaseTest:
    def setup(self):
        print("Setup from BaseTest")

class LoginTest(BaseTest):
    def run(self):
        print("Running Login Test")

class SignupTest(BaseTest):
    def run(self):
        print("Running Signup Test")



LoginTest().setup()
LoginTest().run()
SignupTest().setup()
SignupTest().run()
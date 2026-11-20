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

# More complex: a shared template method in the base class that each sibling
# fills in - the classic hierarchical design used by real test frameworks.
class BaseTest2:
    name = "base"

    def setup(self):
        print(f"{self.name}: setup")

    def teardown(self):
        print(f"{self.name}: teardown")

    def execute(self):
        # Template method: subclasses only supply the actual test steps.
        self.setup()
        try:
            self.test_steps()
        finally:
            self.teardown()

    def test_steps(self):
        raise NotImplementedError("subclasses must implement test_steps()")


class LoginTest2(BaseTest2):
    name = "login"

    def test_steps(self):
        print("login: entering credentials and submitting")


class SignupTest2(BaseTest2):
    name = "signup"

    def test_steps(self):
        print("signup: filling the registration form")


for test_class in (LoginTest2, SignupTest2):
    test_class().execute()

# Siblings are independent: changing one class does not affect the other.
print("shared parent:", BaseTest2.name, "| siblings:", LoginTest2.name, SignupTest2.name)
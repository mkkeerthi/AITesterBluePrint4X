# 142_ML.py
# Multilevel inheritance: UITest -> BaseTest -> TestSuite. UITest's run() calls
# info() from the grandparent class and setup() from the parent class.
class TestSuite:
    def info(self):
        print("This is GF - Step 1")


class BaseTest(TestSuite):
    def setup(self):
        print("BaseTest - F - Step 2")


class UITest(BaseTest):
    def run(self):
        self.info()
        self.setup()
        print("Running Test Case")


test = UITest()
test.run()

# More complex: three levels with constructors and overrides, showing how a
# method call climbs the chain and how super() connects each level.
class TestSuite2:
    def __init__(self, suite_name):
        self.suite_name = suite_name
        print(f"TestSuite2 init ({self.suite_name})")

    def info(self):
        return f"suite={self.suite_name}"

    def setup(self):
        print(" grandparent setup")


class BaseTest2(TestSuite2):
    def __init__(self, suite_name, browser):
        super().__init__(suite_name)
        self.browser = browser
        print(f"BaseTest2 init ({self.browser})")

    def setup(self):
        super().setup()
        print(" parent setup")


class UITest2(BaseTest2):
    def __init__(self, suite_name, browser, url):
        super().__init__(suite_name, browser)
        self.url = url

    def setup(self):
        super().setup()
        print(" child setup")

    def run(self):
        self.setup()
        print(f"running on {self.url} [{self.info()}]")


uit = UITest2("nightly", "chrome", "https://example.com")
uit.run()

# Every setup() in the chain ran, in grandparent -> parent -> child order.
print("MRO:", [cls.__name__ for cls in UITest2.__mro__])
print("attributes from all levels:", uit.__dict__)
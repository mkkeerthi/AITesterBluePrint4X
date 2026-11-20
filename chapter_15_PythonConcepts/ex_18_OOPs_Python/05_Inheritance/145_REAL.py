# 145_REAL.py
# Real-world inheritance with a constructor: BaseTest stores the browser, and
# LoginTest/SignupTest inherit it, so setup() launches whichever browser each
# subclass object was created with.
class BaseTest:
    def __init__(self, browser):
        self.browser = browser

    def setup(self):
        print(f"Launching {self.browser}")

class LoginTest(BaseTest):
    def run_test(self):
        self.setup()
        print("Running login test...")


class SignupTest(BaseTest):
    def run_test(self):
        self.setup()
        print("Running signup test...")

t = LoginTest("chrome")
t.run_test()

t = SignupTest("firefox")
t.run_test()

# More complex: a shared run() template in the base, with hooks that
# subclasses override; plus a fixture-style class that builds test objects.
class BaseTest2:
    def __init__(self, browser="chrome", headless=False):
        self.browser = browser
        self.headless = headless

    def setup(self):
        mode = "headless" if self.headless else "headed"
        return f"launching {self.browser} ({mode})"

    def teardown(self):
        return f"closing {self.browser}"

    def execute(self):
        print(self.setup())
        try:
            self.run_test()
        finally:
            print(self.teardown())

    def run_test(self):
        raise NotImplementedError


class LoginTest2(BaseTest2):
    def run_test(self):
        print("  login test steps")


class SignupTest2(BaseTest2):
    def run_test(self):
        print("  signup test steps")


# A small factory keeps test creation in one place.
def make_test(kind, **options):
    mapping = {"login": LoginTest2, "signup": SignupTest2}
    return mapping[kind](**options)


for kind in ["login", "signup"]:
    make_test(kind, browser="edge", headless=True).execute()
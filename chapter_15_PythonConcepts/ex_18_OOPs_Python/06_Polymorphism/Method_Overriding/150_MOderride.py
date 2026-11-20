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

# More complex: polymorphism in a loop - the SAME call runs different code
# depending on the object's actual class, plus super() to extend rather than
# replace the parent behaviour.
class LoginTest2(BaseTest):
    def run(self):
        super().run()
        print("  + Runnning Login Test")


class SignupTest(BaseTest):
    def run(self):
        print("Runnning Signup Test")


tests = [BaseTest(), LoginTest(), LoginTest2(), SignupTest()]
for test in tests:
    print(f"{type(test).__name__}:", end=" ")
    test.run()

# The method actually called depends on the object, not the variable type.
print("same call, different output above")

# Overriding also works through an instance placed in a list of the parent type.
print("all are BaseTest instances:", all(isinstance(x, BaseTest) for x in tests))
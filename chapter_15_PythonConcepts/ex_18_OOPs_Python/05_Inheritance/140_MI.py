# 140_MI.py
# Multiple inheritance: TestHybrid inherits from both APIBase and DBBase, so
# one object can call api_auth() and db_connect() as well as its own run().
class APIBase:
    def api_auth(self):
        print("Authenticatin API")

class DBBase:
    def db_connect(self):
        print("Connecting to the DB")


class TestHybrid(APIBase, DBBase):
    def run(self):
        self.api_auth()
        self.db_connect()
        print("Test Case Running.")

tc1 = TestHybrid()
tc1.run()

# More complex: constructors in multiple inheritance, super() chaining, and
# the MRO that decides which parent's method wins.
class APIBase2:
    def __init__(self):
        print("APIBase2 init")
        self.api_ready = True

    def api_auth(self):
        print("Authenticating API")


class DBBase2:
    def __init__(self):
        print("DBBase2 init")
        self.db_ready = True

    def db_connect(self):
        print("Connecting to the DB")


class HybridTest(APIBase2, DBBase2):
    def __init__(self):
        # With cooperative parents, one super() call reaches both.
        super().__init__()
        self.name = "hybrid"

    def run(self):
        self.api_auth()
        self.db_connect()
        print(f"running {self.name}: api_ready={self.api_ready}, db_ready={getattr(self, 'db_ready', False)}")


h = HybridTest()
h.run()

# super() only initialised the FIRST parent because DBBase2.__init__ does not
# call super(). Calling both explicitly fixes it:
class HybridTest2(APIBase2, DBBase2):
    def __init__(self):
        APIBase2.__init__(self)
        DBBase2.__init__(self)


h2 = HybridTest2()
print("MRO:", [cls.__name__ for cls in HybridTest2.__mro__])
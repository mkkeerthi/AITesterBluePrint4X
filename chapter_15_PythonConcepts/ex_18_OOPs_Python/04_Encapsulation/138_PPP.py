# 138_PPP.py
# Public / protected / private members in a test-automation class: driver is
# public, _config is protected by convention, __api__key is private. Private
# methods are called internally by work(); the trailing comments summarize access.
class TestExample:
    def __init__(self):
        self.driver = "Chrome"
        self._config = "STAG"
        self.__api__key = "ABC12345"

    def show(self):
        print(f"Driver: {self.driver}")
        print(f"Config: {self._config}")
        print(f"API Key: {self.__api__key}")


    def __private_method1(self):
        pass

    def __private_method2(self):
        pass

    def work(self):
        self.__private_method1()
        self.__private_method2()


obj = TestExample()
obj.show()
obj.work()

# More complex: the same access levels put to work in a real test object -
# a public API, a protected config, a private helper, and an audit log.
class ApiTest:
    BASE_URL = "https://api.example.com"      # class constant

    def __init__(self, token):
        self.token = token                    # public
        self._timeout = 30                    # protected
        self.__attempts = 0                   # private
        self._audit = []

    def get(self, path):
        self.__attempts += 1                  # private state
        self._audit.append(f"GET {path}")
        return {"path": path, "status": 200, "attempt": self.__attempts}

    def audit_log(self):
        return list(self._audit)

    def __check_token(self):
        # Private helper: only this class calls it.
        return bool(self.token)


t = ApiTest("abc123")
print(t.get("/users"), t.get("/orders"))
print("attempts (private):", t._ApiTest__attempts)
print("audit:", t.audit_log())
print("token valid:", t._ApiTest__check_token())


# Access levels:
# print(obj.driver)          # ✅ Public — accessible
# print(obj._config)         # ⚠️ Protected — accessible but discouraged
# print(obj.__api__key)     # ❌ Private — AttributeError

# Note: __api__key is name-mangled to _TestExample__api__key, because mangling
# applies to any name with two leading underscores that does not end in two.
print("mangled name in __dict__:", obj._TestExample__api__key)


# Access levels:
# print(obj.driver)          # ✅ Public — accessible
# print(obj._config)         # ⚠️ Protected — accessible but discouraged
# print(obj.__api__key)     # ❌ Private — AttributeError
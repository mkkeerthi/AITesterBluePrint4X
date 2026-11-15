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


# Access levels:
# print(obj.driver)          # ✅ Public — accessible
# print(obj._config)         # ⚠️ Protected — accessible but discouraged
# print(obj.__api__key)     # ❌ Private — AttributeError
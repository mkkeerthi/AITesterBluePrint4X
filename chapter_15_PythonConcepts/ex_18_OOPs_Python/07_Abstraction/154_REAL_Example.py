# 154_REAL_Example.py
# Practical abstraction for test automation: BrowserManger forces subclasses to
# implement start(), while providing a shared concrete stop(). ChromeBrowser
# supplies start() and inherits stop().
from abc import ABC, abstractmethod

class BrowserManger(ABC):
    @abstractmethod
    def start(self):
        pass

    def stop(self):
        print("Stop command, common")

class ChromeBrowser(BrowserManger):
    def start(self):
        # t = ChromeDriver()
        print("We are starting the chrome")

tc = ChromeBrowser()
tc.start()
tc.stop()

# More complex: a second browser, a driver factory, and a base class that
# provides shared navigation on top of the abstract contract.
class FirefoxBrowser(BrowserManger):
    def start(self):
        print("We are starting firefox")

    def stop(self):
        print("Stopping firefox")


class BrowserManger2(BrowserManger):
    def navigate(self, url):
        self.start()
        print(f"navigating to {url}")
        self.stop()


class Chrome2(BrowserManger2):
    def start(self):
        print("starting chrome")


# The abstract start() guarantees this call always exists.
for cls in (Chrome2, FirefoxBrowser):
    obj = cls()
    obj.start()
    obj.stop()

# A tiny factory hides the subclass choice from the test code.
def browser(name):
    mapping = {"chrome": Chrome2, "firefox": FirefoxBrowser}
    try:
        return mapping[name]()
    except KeyError:
        raise ValueError(f"unsupported browser: {name}")


b = browser("chrome")
b.start()
print("is a BrowserManger:", isinstance(b, BrowserManger))

try:
    browser("safari")
except ValueError as error:
    print("ValueError:", error)
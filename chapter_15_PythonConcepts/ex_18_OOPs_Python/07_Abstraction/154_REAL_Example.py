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
# 156_Ex.py
# Abstraction exercise with an inheritance chain: abstract ExcelReader ->
# abstract Browser -> concrete TC1, which implements every abstract method and
# exposes a single runTc() workflow.
from abc import ABC, abstractmethod

class ExcelReader(ABC):

    @abstractmethod
    def readFromExcel(self):
        pass

class Browser(ExcelReader):
    @abstractmethod
    def startBrowser(self):
        pass

    @abstractmethod
    def stopBrowser(self):
        pass


class TC1(Browser):
    def startBrowser(self):
        print("Starting")

    def stopBrowser(self):
        print("Stop")

    def readFromExcel(self):
        print("readFromExcel is ready")

    def runTc(self):
        self.startBrowser()
        self.readFromExcel()
        self.stopBrowser()














tc1 = TC1()
tc1.runTc()

# More complex: generalize the workflow so one base class runs many tests,
# and show the error you get from an incomplete subclass.
class Browser2(ExcelReader):
    def __init__(self, name="chrome"):
        self.name = name

    def startBrowser(self):
        print(f"starting {self.name}")

    def stopBrowser(self):
        print(f"stopping {self.name}")

    def readFromExcel(self):
        print("reading test data from excel")

    def runTc(self):
        self.startBrowser()
        try:
            self.readFromExcel()
            print("executing test steps")
        finally:
            self.stopBrowser()


class DataDrivenTC(Browser2):
    def __init__(self, name, rows):
        super().__init__(name)
        self.rows = rows

    def readFromExcel(self):
        for row in self.rows:
            print(f"row: {row}")


Browser2("firefox").runTc()
DataDrivenTC("chrome", [{"user": "pramod"}, {"user": "amit"}]).runTc()

# A subclass that forgets a method remains abstract and cannot be created.
class BrokenTC(Browser2):
    def startBrowser(self):
        pass


try:
    BrokenTC()
except TypeError as error:
    print("TypeError:", error)
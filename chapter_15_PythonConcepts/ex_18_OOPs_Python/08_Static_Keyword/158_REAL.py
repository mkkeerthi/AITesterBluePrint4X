# 158_REAL.py
# Static methods as shared utilities: ExcelReader.readExcelFile() and
# MYSQLDBConnection.readMySQLFile() are called directly on the class from
# multiple test cases without creating objects of those helper classes.
class ExcelReader:
    @staticmethod
    def readExcelFile():
        print("Reading from Excel")

class MYSQLDBConnection:

    @staticmethod
    def readMySQLFile():
        print("Reading from MySQL")


class TC1:

    def runTC(self):
        ExcelReader.readExcelFile()
        MYSQLDBConnection.readMySQLFile()
        print("Hi")

class TC2:

    def runTC(self):
        ExcelReader.readExcelFile()
        MYSQLDBConnection.readMySQLFile()
        print("Hi")

tc1 = TC1()
tc2 = TC1()
tc1.runTC()
tc2.runTC()

# More complex: a config-aware utility class where the static method takes
# arguments, plus a classmethod factory and a counter shared across tests.
class ExcelReader2:
    files_read = 0

    @staticmethod
    def read_excel_file(path, sheet="Sheet1"):
        ExcelReader2.files_read += 1
        return [{"row": 1, "sheet": sheet, "file": path}]

    @classmethod
    def stats(cls):
        return f"{cls.files_read} file(s) read"


class TestRunner:
    def __init__(self, name):
        self.name = name
        self.rows = []

    def load(self, path):
        self.rows = ExcelReader2.read_excel_file(path)
        return self

    def run(self):
        print(f"{self.name}: {len(self.rows)} row(s) from {self.rows[0]['file']}")
        return len(self.rows)


TestRunner("TC1").load("data/login.xlsx").run()
TestRunner("TC2").load("data/signup.xlsx").run()
print(ExcelReader2.stats())

# Because the readers are static, a module-level function works just as well:
read = ExcelReader2.read_excel_file
print(read("data/orders.xlsx", sheet="Orders"))
print(ExcelReader2.stats())
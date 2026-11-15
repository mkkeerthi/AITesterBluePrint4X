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
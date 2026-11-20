# 136_Ecap.py
# Encapsulation in a real scenario: Bank keeps the balance public but makes the
# account number private (__account_number). Balance can be deposited/checked,
# while the account number is only revealed by show_me_account_number(True);
# direct access to icici.__account_number fails.
class Bank:

    def __init__(self, account_number, balance):
        self.balance = balance  # public
        self.__account_number = account_number  # Private

    def check_balance(self):
        print(self.balance)

    def deposit(self, amount):
        self.balance = self.balance + amount

    def show_me_account_number(self, is_auth):
        if is_auth == True:
            print(self.__account_number)
        else:
            print("Not Allowed!")


icici = Bank(9876543210, 100)
icici.deposit(100)
icici.check_balance()
# print(icici.__account_number)
# if you are cashier you can see the a/c becoz of the ecapsulation.
icici.show_me_account_number(True)

# More complex: withdraw guarded by a balance check, an audit log, and a
# demonstration of how the private attribute is really stored.
class BankAccount:
    def __init__(self, account_number, balance=0):
        self.__account_number = account_number     # private
        self.balance = balance                     # public
        self._transactions = []                    # protected by convention

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.balance += amount
        self._transactions.append(("deposit", amount))
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("withdraw must be positive")
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount
        self._transactions.append(("withdraw", amount))
        return self.balance

    def statement(self):
        lines = [f"account {self.__masked()}"]
        lines += [f"  {kind:<8} {amount}" for kind, amount in self._transactions]
        lines.append(f"  balance  {self.balance}")
        return "\n".join(lines)

    def __masked(self):
        # Only the last four digits are ever shown.
        return f"****{str(self.__account_number)[-4:]}"


acc = BankAccount(9876543210, 100)
acc.deposit(50)
try:
    acc.withdraw(500)
except ValueError as error:
    print("rejected:", error)
acc.withdraw(30)
print(acc.statement())

# From outside the class, the private name does not exist...
try:
    acc.__account_number
except AttributeError as error:
    print("AttributeError:", error)
# ...but Python does not truly hide it - name mangling just renames it.
print("mangled:", acc._BankAccount__account_number)
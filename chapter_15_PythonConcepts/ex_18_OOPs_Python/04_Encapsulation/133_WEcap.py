# 133_WEcap.py
# Login example without encapsulation: a VWOLoginPage object stores the email
# and password as plain public attributes and compares them with hard-coded
# values (insecure - the credentials are visible in source code).
class VWOLoginPage:
    def __init__(self,email_arg,password_arg):
        self.email = email_arg
        self.password = password_arg

    def login_confirm(self):
        if self.email == "student@example.com" and self.password == "demo123":
            print("Allowed to Login")
        else:
            print("Login Failed")


email = input("Enter the vwo login email ")
password = input("Enter the vwo login password ")

vwo_object_ref = VWOLoginPage(email,password)
vwo_object_ref.login_confirm()

# More complex: the same login, but with credentials injected instead of
# hard-coded, so tests can run without a keyboard.
class VWOLoginPage2:
    VALID_EMAIL = "student@example.com"
    VALID_PASSWORD = "demo123"

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def login_confirm(self):
        if self.email == self.VALID_EMAIL and self.password == self.VALID_PASSWORD:
            return True
        return False


# Data-driven checks - the usual shape of a login test.
cases = [
    ("student@example.com", "demo123", True),
    ("student@example.com", "wrong", False),
    ("other@example.com", "demo123", False),
    ("", "", False),
]

for email, password, expected in cases:
    page = VWOLoginPage2(email, password)
    result = page.login_confirm()
    status = "ok" if result == expected else "MISMATCH"
    print(f"{email or '(blank)':<22} {password or '(blank)':<9} -> {result} [{status}]")
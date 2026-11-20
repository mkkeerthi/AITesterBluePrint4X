# 134_WEcap_Secure.py
# Improved version of 133: credentials are loaded from a .env file with
# python-dotenv (os.getenv) instead of being hard-coded, so secrets stay out of
# the code. Also prints the stored password and os.name.
from dotenv import load_dotenv
import os
class VWOLoginPage:

    def __init__(self, email_arg, password_arg):

        self.email = email_arg
        self.password = password_arg

    def login_confirm(self):
        load_dotenv()
        if self.email == os.getenv("USERNAME") and self.password == os.getenv("PASSWORD"):
            print("Allowed, Login Sucess")
        else:
            print("Login Failed")


email = input("Enter the vwo login email ")
password = input("Enter the vwo login password ")

vwo_object_ref = VWOLoginPage(email,password)
vwo_object_ref.login_confirm()
print(vwo_object_ref.password)

print(os.name)

# More complex: keep secrets off the object entirely - the class reads the
# environment when it needs them, and a fallback keeps the demo runnable
# without a real .env file.
class VWOLoginPage2:
    def __init__(self, email, password):
        self._email = email
        self._password = password

    def login_confirm(self):
        expected_email = os.getenv("USERNAME", "student@example.com")
        expected_password = os.getenv("PASSWORD", "demo123")
        return self._email == expected_email and self._password == expected_password

    def __repr__(self):
        # Never include the password in a repr/log line.
        return f"VWOLoginPage2(email={self._email!r}, password=<hidden>)"


# Credentials from env vars (falling back to the demo values above).
env_email = os.getenv("USERNAME", "student@example.com")
env_password = os.getenv("PASSWORD", "demo123")

page = VWOLoginPage2(env_email, env_password)
print("login ok:", page.login_confirm())
print(page)

# A missing env var is a common real-world failure - show how to detect it.
if os.getenv("PASSWORD") is None:
    print("PASSWORD not set in the environment; using the demo fallback")
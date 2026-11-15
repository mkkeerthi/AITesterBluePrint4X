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
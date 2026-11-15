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
# 171_Custom_Exception.py
# Raising exceptions with raise: vwo_login() raises a generic Exception when the
# user is not "admin" (uncomment the first call to see it) and returns a welcome otherwise.
def vwo_login(user):
    if user!= "admin":
        raise Exception("You are not admin, not auth.")
    return "Welcome Admin"

# print(vwo_login("pramod"))
print(vwo_login("admin"))
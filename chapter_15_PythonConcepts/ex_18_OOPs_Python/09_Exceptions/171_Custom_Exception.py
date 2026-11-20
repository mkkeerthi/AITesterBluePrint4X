# 171_Custom_Exception.py
# Raising exceptions with raise: vwo_login() raises a generic Exception when the
# user is not "admin" (uncomment the first call to see it) and returns a welcome otherwise.
def vwo_login(user):
    if user!= "admin":
        raise Exception("You are not admin, not auth.")
    return "Welcome Admin"

# print(vwo_login("pramod"))
print(vwo_login("admin"))

# More complex: raise the built-in exception that fits, and define proper
# custom exception classes instead of a bare Exception.
class NotAdminError(Exception):
    """Raised when a non-admin user tries an admin-only action."""


def vwo_login2(user, password=None):
    if user != "admin":
        raise NotAdminError(f"{user!r} is not an admin")
    if password is not None and password != "secret":
        raise PermissionError("wrong password")
    return "Welcome Admin"


# Prove the failure branch and catch the specific types.
try:
    print(vwo_login2("pramod"))
except NotAdminError as error:
    print("NotAdminError:", error)

try:
    print(vwo_login2("admin", "wrong"))
except PermissionError as error:
    print("PermissionError:", error)

print(vwo_login2("admin"))
print(vwo_login2("admin", "secret"))

# Check the exception hierarchy: NotAdminError is an Exception subclass.
print("subclass of Exception:", issubclass(NotAdminError, Exception))
print("in the MRO:", [c.__name__ for c in NotAdminError.__mro__])
# 177_Util.py
# Entry point of the package example: imports two modules from the "package"
# folder and calls the function each one defines.
from package import util_module,util_module2

util_module2.blahblah("das")
util_module.blah("das")

# More complex: import through the package's public API, and use the helpers
# and the class defined in the two modules.
import package
from package import slugify, is_valid_email, Settings

print(package.__version__)
print(package.package_info())

print(slugify("Login Page Automation"))
print(is_valid_email("qa@example.com"), is_valid_email("qa@com"))

settings = Settings(env="staging", browser="firefox")
print(settings)
print(settings.as_dict())

# The two original helpers still work exactly as before.
util_module.blah("via module attribute")
util_module2.blahblah("via module attribute")

# __all__ controls what "from package import *" brings in.
namespace = {}
exec("from package import *", namespace)
print("star-import names:", sorted(k for k in namespace if not k.startswith("__")))
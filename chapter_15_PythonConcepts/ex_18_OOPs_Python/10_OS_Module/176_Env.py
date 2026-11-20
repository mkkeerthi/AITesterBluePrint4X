# 176_Env.py
# Reads an environment variable with os.getenv(): prints the value of TOKEN
# (or None if it is not set), the usual way to keep secrets out of code.
import os
print( os.getenv("TOKEN"))

# More complex: required vs optional settings, defaults, and a clear error
# when a mandatory variable is missing. Nothing here needs a real .env file.
REQUIRED = ["TOKEN", "BASE_URL"]
OPTIONAL = {"TIMEOUT": "30", "RETRIES": "3"}

missing = [name for name in REQUIRED if not os.getenv(name)]
print("missing required:", missing or "none")

config = {name: os.getenv(name, "(not set)") for name in REQUIRED}
config.update({name: os.getenv(name, default) for name, default in OPTIONAL.items()})
print("config:", config)

# A helper that fails fast with a useful message.
def require(name):
    value = os.getenv(name)
    if not value:
        raise EnvironmentError(f"environment variable {name} is required")
    return value


try:
    print("BASE_URL =", require("BASE_URL"))
except EnvironmentError as error:
    print("EnvironmentError:", error)

# Setting a variable for this process only (children would inherit it).
os.environ["DEMO_MODE"] = "1"
print("DEMO_MODE:", os.getenv("DEMO_MODE"))
print("as int:", int(os.getenv("DEMO_MODE", "0")))

# Listing every environment variable, filtered, without dumping secrets.
interesting = {k: v for k, v in os.environ.items() if k.startswith("DEMO_")}
print("DEMO_ variables:", interesting)

# Never print real secrets; mask them instead.
def mask(value, keep=2):
    return value[:keep] + "*" * max(0, len(value) - keep)


token = os.getenv("DEMO_MODE", "")
print("masked token:", mask(token))
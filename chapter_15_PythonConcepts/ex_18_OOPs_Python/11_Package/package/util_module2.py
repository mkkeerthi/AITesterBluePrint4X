# util_module2.py
# Second helper module in the package: defines blahblah(name), which prints the name.
def blahblah(name):
    print(name)

# More complex: share state through module-level constants and provide a
# class that other modules can import and reuse.
DEFAULT_TIMEOUT = 30
SUPPORTED_BROWSERS = ("chrome", "firefox", "edge")


class Settings:
    def __init__(self, env="qa", browser="chrome", timeout=DEFAULT_TIMEOUT):
        if browser not in SUPPORTED_BROWSERS:
            raise ValueError(f"unsupported browser: {browser}")
        self.env = env
        self.browser = browser
        self.timeout = timeout

    def as_dict(self):
        return {"env": self.env, "browser": self.browser, "timeout": self.timeout}

    def __repr__(self):
        return f"Settings({self.env!r}, {self.browser!r}, {self.timeout})"


__all__ = ["blahblah", "Settings", "DEFAULT_TIMEOUT", "SUPPORTED_BROWSERS"]

if __name__ == "__main__":
    print(Settings())
    try:
        Settings(browser="safari")
    except ValueError as error:
        print("ValueError:", error)
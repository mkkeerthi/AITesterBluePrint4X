# util_module.py
# Simple helper module inside the package: defines blah(name), which prints the name.
def blah(name):
    print(name)

# More complex: real helpers - a slug builder and a simple validator - showing
# what a package module is actually for (reusable code, no printing by default).
def slugify(text):
    """Turn 'API Test Automation' into 'api-test-automation'."""
    cleaned = "".join(c.lower() if c.isalnum() else "-" for c in text.strip())
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-")


def is_valid_email(email):
    if not isinstance(email, str) or email.count("@") != 1:
        return False
    local, _, domain = email.partition("@")
    return bool(local) and "." in domain and not domain.startswith(".") and not domain.endswith(".")


def truncate(text, length=20):
    """Return text shortened to `length` characters, with an ellipsis."""
    return text if len(text) <= length else text[: length - 1] + "\u2026"


if __name__ == "__main__":
    # Only runs when the module is executed directly, not when imported.
    print(slugify("API Test  Automation"))
    print(is_valid_email("pramod@example.com"), is_valid_email("bad-email"))
    print(truncate("a very long test case name", 12))

    
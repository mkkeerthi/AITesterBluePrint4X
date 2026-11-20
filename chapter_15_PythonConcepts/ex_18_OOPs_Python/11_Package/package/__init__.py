# __init__.py
# Marks this directory as a Python package so its modules can be imported
# (e.g. "from package import util_module"). The file itself is left empty.

# More complex: a package's __init__.py can expose a convenient public API,
# so callers can "from package import slugify" without knowing the layout.
__version__ = "1.0.0"

try:
    # Normal case: this file is imported as part of the package.
    from .util_module import slugify, is_valid_email, truncate
    from .util_module2 import Settings, DEFAULT_TIMEOUT, SUPPORTED_BROWSERS
except ImportError:
    # Fallback so the file can also be run directly from its own folder.
    from util_module import slugify, is_valid_email, truncate
    from util_module2 import Settings, DEFAULT_TIMEOUT, SUPPORTED_BROWSERS

__all__ = [
    "slugify",
    "is_valid_email",
    "truncate",
    "Settings",
    "DEFAULT_TIMEOUT",
    "SUPPORTED_BROWSERS",
    "__version__",
]


def package_info():
    return f"package v{__version__} | browsers: {', '.join(SUPPORTED_BROWSERS)}"

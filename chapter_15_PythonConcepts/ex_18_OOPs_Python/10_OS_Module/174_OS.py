# 174_OS.py
# Tour of the os module: prints the OS name, current working directory and
# directory contents, and demonstrates creating, removing and renaming files/folders.
import os
print(os.name)
print(os.getcwd())
# print(os.mkdir("AI"))
print(os.listdir())

# These two lines assume AI.txt exists, so they are guarded here to keep the
# file runnable on any machine.
if os.path.exists("AI.txt"):
    print(os.remove("AI.txt"))
    print(os.rename("AI.txt","testdata.txt"))
else:
    print("AI.txt does not exist - skipping remove/rename")

# More complex: a safe workflow with pathlib-free os calls, all inside a
# temporary folder so nothing is left behind.
import tempfile
import shutil

workdir = tempfile.mkdtemp(prefix="os_demo_")
try:
    print("temp dir:", workdir)

    # Build paths portably with os.path.join.
    nested = os.path.join(workdir, "reports", "2026")
    os.makedirs(nested, exist_ok=True)

    data_file = os.path.join(nested, "summary.txt")
    with open(data_file, "w", encoding="utf-8") as handle:
        handle.write("all tests passed")

    print("exists:", os.path.exists(data_file))
    print("is file:", os.path.isfile(data_file), "| is dir:", os.path.isdir(nested))
    print("size:", os.path.getsize(data_file), "bytes")
    print("basename:", os.path.basename(data_file))
    print("dirname:", os.path.dirname(data_file))
    print("split:", os.path.split(data_file))

    # Walk the tree top-down - the standard way to scan folders.
    for root, dirs, files in os.walk(workdir):
        for name in files:
            print("found:", os.path.relpath(os.path.join(root, name), workdir))

    # Environment and path helpers.
    print("env HOME/USERPROFILE set:", bool(os.getenv("HOME") or os.getenv("USERPROFILE")))
    print("path separator:", os.sep, "| pathsep:", os.pathsep)
finally:
    # Cleanup: remove the whole tree, even if something above failed.
    shutil.rmtree(workdir, ignore_errors=True)
    print("cleaned up:", not os.path.exists(workdir))


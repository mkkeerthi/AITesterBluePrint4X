# 175.OS2py
# Practical os module workflow: builds paths with os.path.join, creates a folder
# with os.makedirs, writes a file into it, reports existence/size/listing, and
# then deletes the file and folder (cleanup).
import os

print("CWD:", os.getcwd())
print("OS:", os.name)

folder = os.path.join(os.getcwd(), "demo_output")
print(folder)

os.makedirs(folder, exist_ok=True)

file_path = os.path.join(folder, "hello.txt")
with open(file_path, "w") as f:
    f.write("Hello from the os module")


print("Exists?", os.path.exists(file_path))
print("Size:", os.path.getsize(file_path), "bytes")
print("Files:", os.listdir(folder))

os.remove(file_path)
os.rmdir(folder)
print("Cleaned up:", not os.path.exists(folder))

# More complex: the same workflow with a try/finally so cleanup always
# happens, plus os.walk, pathlib comparison and JSON round-tripping.
import json
import shutil

folder = os.path.join(os.getcwd(), "demo_output_2")
try:
    os.makedirs(os.path.join(folder, "logs"), exist_ok=True)

    config_path = os.path.join(folder, "config.json")
    with open(config_path, "w", encoding="utf-8") as handle:
        json.dump({"env": "qa", "browsers": ["chrome", "firefox"]}, handle, indent=2)

    log_path = os.path.join(folder, "logs", "run.log")
    with open(log_path, "w", encoding="utf-8") as handle:
        handle.write("started\nfinished\n")

    for root, dirs, files in os.walk(folder):
        for name in sorted(files):
            full = os.path.join(root, name)
            print(f"{os.path.relpath(full, folder):<20} {os.path.getsize(full):>3} bytes")

    with open(config_path, encoding="utf-8") as handle:
        print("config:", json.load(handle))

    # pathlib does the same join/exists work in an object-oriented style.
    from pathlib import Path
    root = Path(folder)
    print("pathlib listing:", sorted(p.name for p in root.rglob("*") if p.is_file()))
finally:
    shutil.rmtree(folder, ignore_errors=True)
    print("Cleaned up:", not os.path.exists(folder))

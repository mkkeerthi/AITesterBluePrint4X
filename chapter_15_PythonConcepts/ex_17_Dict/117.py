# 117.py
# Creates a student dictionary, reads values by key, and shows that assigning
# to an existing key simply overwrites its value (age changed to 100).
student_infor = {
    "name": "Pramod",
    # "age": 65,
    "age": 67,
    "address": "KA"
}

print(student_infor)

print(student_infor["name"])
print(student_infor["age"])

print(student_infor["address"])
student_infor["age"] = 100
print(student_infor)

# More complex: add new keys, merge dicts, and the copy-vs-alias trap that
# catches people when nesting is involved.
student_infor["graduated"] = False              # a new key is simply added
student_infor.setdefault("city", "Bangalore")   # only sets if absent
print(student_infor)

extra = {"score": 88, "grade": "A"}
student_infor.update(extra)
print(student_infor)

# | merges into a NEW dict (3.9+); |= updates in place.
merged = {**student_infor, "verified": True}
print("merged:", merged)
print("original untouched:", "verified" in student_infor)

# A shallow copy shares nested objects, so changes to a nested dict are visible.
import copy

shallow = student_infor.copy()
deep = copy.deepcopy(student_infor)
student_infor["nested"] = {"a": 1}
shallow["nested"] = {"a": 1}
shallow["nested"]["a"] = 99
print("shallow sees change:", shallow["nested"], "original has no nested key:", "nested" in student_infor)

# Keys must be hashable; values can be anything.
print({1: "int key", (1, 2): "tuple key", "name": ["list", "value"]})
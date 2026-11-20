# 119_Dict_Nested.py
# A list of three nested student dictionaries; shows accessing a specific
# record's nested office address as student_list[2]["address"]["office_address"].
student_infor1 = {
    "name": "Pramod",
    # "age": 65,
    "age": 67,
    "address": {
        "home_address": "ND",
        "office_address": "KA"
    }
}

student_infor2 = {
    "name": "Amit",
    # "age": 65,
    "age": 69,
    "address": {
        "home_address": "GOA",
        "office_address": "KA"
    }
}

student_infor3 = {
    "name": "Murthy",
    # "age": 65,
    "age": 120,
    "address": {
        "home_address": "PODI",
        "office_address": "vizag"
    }
}

student_list = [student_infor1,student_infor2,student_infor3]
print(student_list)
print(student_list[2]["address"]["office_address"])

# More complex: find a record by name, update it, and build a lookup dict
# so repeated access is O(1) instead of a linear scan.
wanted = "Murthy"
match = next((s for s in student_list if s["name"] == wanted), None)
if match:
    match["age"] = 121
print([s["age"] for s in student_list])

by_name = {s["name"]: s for s in student_list}
print(by_name["Amit"]["address"]["home_address"])

# A summary report built from the list of records.
oldest = max(student_list, key=lambda s: s["age"])
print(f"oldest: {oldest['name']} ({oldest['age']})")
print(f"average age: {sum(s['age'] for s in student_list) / len(student_list):.1f}")

# Removing a key from every record, and guarding with pop()'s default.
for student in student_list:
    student.pop("address", None)
print(student_list[0])

# Merging two records: dict.update wins on conflicts.
base = {"name": "Pramod", "age": 67, "country": "IN"}
override = {"age": 68, "role": "SDET"}
print({**base, **override})
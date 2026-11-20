# 118_Dict_Multiple.py
# Nested dictionaries: each student has an inner "address" dictionary. Two
# students are kept in a list, and nested data is read with chained keys.
student_infor1 = {
    "name": "Pramod",
    "age": 67,
    "address": {
        "home_address": "ND",
        "office_address": "KA"
    }
}
student_infor2 = {
    "name": "Amit",
    "age": 69,
    "address": {
        "home_address": "GOA",
        "office_address": "KA"
    }
}


student_list = [student_infor1,student_infor2]
print(student_list)
print(student_list[0])
print(student_list[0]["name"])
print(student_list[0]["address"]["office_address"])

# More complex: report over every student, handle a missing nested key
# safely, and update one field per record.
for student in student_list:
    # get() with a default avoids KeyError when a key is missing
    city = student.get("address", {}).get("home_address", "unknown")
    print(f"{student['name']:<8} age={student['age']:<4} home={city}")

# Add a derived key to every record.
for student in student_list:
    student["adult"] = student["age"] >= 18
print(student_list[1])

# Filtering records with a nested condition.
in_ka = [s["name"] for s in student_list if s["address"]["office_address"] == "KA"]
print("office in KA:", in_ka)

# Sorting records by a nested field.
by_age = sorted(student_list, key=lambda s: s["age"])
print([s["name"] for s in by_age])

# Count records per office city using a dict.
tally = {}
for student in student_list:
    office = student["address"]["office_address"]
    tally[office] = tally.get(office, 0) + 1
print(tally)
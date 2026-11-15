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
# 111_IQ.py
# Uses map() with a named function to convert every name in a list to uppercase.
name = ["pramod", "dutta", "qa", "lucky"]

def upper_case(string):
    return string.upper()


upper_name_list = list(map(upper_case, name))
print(upper_name_list)
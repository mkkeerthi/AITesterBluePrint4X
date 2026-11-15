# 48.py
# match/case on an HTTP-like status code, grouping 200|201 as success and
# using _ as the fallback for any unknown status.
status = 900

match status:
    case 200 | 201:
        print("Request successful")
    case 400:
        print("Bad request")
    case 401:
        print("Unauthorized")
    case 500:
        print("Server error")
    case _:
        print("Unknown status")
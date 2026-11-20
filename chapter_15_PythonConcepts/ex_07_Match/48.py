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

# More complex: status handling with guards that classify by hundreds,
# the way an HTTP client usually does it.
def http_result(code):
    match code:
        case int(c) if 200 <= c < 300:
            return "success"
        case int(c) if 300 <= c < 400:
            return "redirect"
        case int(c) if 400 <= c < 500:
            return "client error"
        case int(c) if 500 <= c < 600:
            return "server error"
        case _:
            return "invalid"


for code in [200, 204, 301, 404, 503, 900, "200"]:
    print(f"{str(code):>5} -> {http_result(code)}")
# 149_IQ.py
# Interview example: instead of overloading make_http_request(), a single method
# uses a default auth=None parameter to handle both authenticated and anonymous requests.
class Browser:

    def make_http_request(self, url):
        print("Hi, Lets make the HTTP request without auth", url)

    def make_http_request(self, url, auth=None):
        print("Hi, Lets make the HTTP request with auth", url, auth)


t = Browser()
t.make_http_request("google.com","admin")

# More complex: the clean way to express the same thing - an optional auth
# that changes the behaviour, plus separate methods when the flows differ a lot.
class APIClient:
    def __init__(self):
        self.calls = []

    def make_http_request(self, url, auth=None, timeout=30):
        self.calls.append((url, auth, timeout))
        if auth:
            return f"GET {url} as {auth} (timeout {timeout}s)"
        return f"GET {url} anonymously (timeout {timeout}s)"


client = APIClient()
print(client.make_http_request("google.com"))
print(client.make_http_request("google.com", "admin"))
print(client.make_http_request("google.com", auth="admin", timeout=5))
print("calls:", client.calls)

# When behaviour is genuinely different, prefer explicit names over one
# overload-like method.
class APIClient2(APIClient):
    def get_public(self, url):
        return self.make_http_request(url)

    def get_private(self, url, token):
        if not token:
            raise ValueError("token required")
        return self.make_http_request(url, auth=token)


c2 = APIClient2()
print(c2.get_public("example.com"))
print(c2.get_private("example.com", "secret"))
try:
    c2.get_private("example.com", "")
except ValueError as error:
    print("ValueError:", error)
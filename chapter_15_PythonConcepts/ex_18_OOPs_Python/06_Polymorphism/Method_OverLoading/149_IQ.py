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
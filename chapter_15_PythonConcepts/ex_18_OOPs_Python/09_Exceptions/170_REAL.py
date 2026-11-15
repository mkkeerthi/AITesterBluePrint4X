# 170_REAL.py
# Real-world exception handling with the requests library: makes an HTTP GET
# and catches ConnectionError, Timeout, and any other Exception, printing the
# status code on success.
import requests

try:
    url = input("Enter the url")
    response = requests.get(url=url)
    print(response.status_code)
except requests.exceptions.ConnectionError:
    print("Exception due to connection error")
except requests.exceptions.Timeout:
    print("Exception due to connection error")
except Exception as e:
    print(e)
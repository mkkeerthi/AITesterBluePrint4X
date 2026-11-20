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

# More complex: a reusable request helper with a timeout, status checking,
# specific error messages and a clear failure type per case.
def fetch(url, timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()          # raise for 4xx/5xx
        return response.json()
    except requests.exceptions.Timeout:
        raise RuntimeError(f"{url} timed out after {timeout}s")
    except requests.exceptions.ConnectionError:
        raise RuntimeError(f"could not connect to {url}")
    except requests.exceptions.HTTPError as error:
        raise RuntimeError(f"{url} returned {error.response.status_code}")
    except requests.exceptions.RequestException as error:
        raise RuntimeError(f"request failed: {error}")


# The network calls are commented out so this file runs offline; the error
# handling still demonstrates the structure.
# for target in ["https://httpbin.org/get", "https://nonexistent.invalid"]:
#     try:
#         print(fetch(target))
#     except RuntimeError as error:
#         print("failed:", error)

# A local-only version of the same idea, proving the control flow:
def fetch_stub(url, mode="ok"):
    if mode == "timeout":
        raise RuntimeError(f"{url} timed out after 5s")
    if mode == "connection":
        raise RuntimeError(f"could not connect to {url}")
    return {"status": "ok", "url": url}


for mode in ["ok", "timeout", "connection", "weird"]:
    try:
        print(fetch_stub("https://example.com", mode))
    except RuntimeError as error:
        print(f"[{mode}] failed: {error}")

# Always be specific in the except order: subclasses first, Exception last.
try:
    raise requests.exceptions.Timeout("slow")
except requests.exceptions.Timeout as error:
    print("specific handler caught:", error)
except Exception:
    print("would only reach here for other errors")
# 112_IQ.py
# Realistic use of map() with a lambda: converts a list of API response times
# from milliseconds to seconds by dividing each value by 1000.
response_times_ms = [1200, 1500, 1800]

# def mil_sec(x):
#     return x / 1000
# response_times_ms_list = list(map(mil_sec, response_times_ms))

response_times_ms_list = list(map(lambda x:x/1000, response_times_ms))
print(response_times_ms_list)

# More complex: compute statistics from mapped values, and flag slow calls.
response_times_ms = [1200, 1500, 1800, 2500, 900]
seconds = [round(t / 1000, 2) for t in response_times_ms]
print(seconds)

average = sum(response_times_ms) / len(response_times_ms)
print(f"average: {average:.0f} ms")

slow = list(filter(lambda t: t > 1500, response_times_ms))
print("slow calls:", slow)

# map + filter together: convert only the slow ones and label them.
converted = list(map(lambda t: f"{t / 1000:.1f}s", filter(lambda t: t > 1500, response_times_ms)))
print("slow calls in seconds:", converted)

# Realistic: pair a metric name with each measurement.
metrics = ["/login", "/search", "/checkout"]
report = list(map(lambda pair: f"{pair[0]} -> {pair[1] / 1000:.2f}s", zip(metrics, response_times_ms[:3])))
for line in report:
    print(line)
# 112_IQ.py
# Realistic use of map() with a lambda: converts a list of API response times
# from milliseconds to seconds by dividing each value by 1000.
response_times_ms = [1200, 1500, 1800]

# def mil_sec(x):
#     return x / 1000
# response_times_ms_list = list(map(mil_sec, response_times_ms))

response_times_ms_list = list(map(lambda x:x/1000, response_times_ms))
print(response_times_ms_list)
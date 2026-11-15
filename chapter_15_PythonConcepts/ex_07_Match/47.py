# 47.py
# Uses Python's match/case statement to map a day number (1-7) to its name.
# Shows OR patterns (case 6 | 7) and the default wildcard case (_).
day = int(input("Enter the day from 1 to 7"))

match day:
    case 1:
        print("Monday")
    case 2:
        print("Tuesday")
    case 3:
        print("Wednesday")
    case 4:
        print("Thursday")
    case 5:
        print("Friday")
    case 6 | 7:
        print("Weekend")
    case _:
        print("Invalid day")
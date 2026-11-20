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

# More complex: match with a guard (if), tuple class-patterns and wildcards,
# wrapped in a function so several values can be tested.
def describe(day):
    match day:
        case 1 | 2 | 3 | 4 | 5:
            print(f"{day} is a weekday")
        case 6 | 7:
            print(f"{day} is the weekend")
        case int(value) if value < 1 or value > 7:
            print(f"{value} is out of range")
        case _:
            print(f"{day!r} is not a number")


for value in [1, 5, 6, 7, 0, 9, "Mon"]:
    describe(value)
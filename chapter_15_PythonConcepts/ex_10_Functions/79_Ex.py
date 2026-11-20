# 79_Ex.py
# Practical *args example: make_pizza(*toppings) accepts any number of topping
# names per person and prints the collected tuple.
def make_pizza(*toppings):
    print(toppings)


pramod = make_pizza("cheese","corn")
yoga = make_pizza("cheese","corn","paneer","capsicm")
vinay = make_pizza("tomato")

# More complex: a real order summary with prices, using *args plus a base
# price and a **kwargs option such as delivery.
def order_summary(*toppings, base=100, **options):
    extra = 20 * len(toppings)
    total = base + extra
    print(f"Toppings: {', '.join(toppings) or 'plain'}")
    print(f"Total: {total}")
    if options.get("delivery"):
        total += options.get("charge", 30)
        print(f"With delivery: {total}")
    return total


order_summary("cheese", "corn")
order_summary("cheese", "paneer", "olives", base=150, delivery=True, charge=40)

# *args can be unpacked from a list, which is handy for data-driven orders.
orders = [
    ("pramod", ["cheese", "corn"]),
    ("yoga", ["cheese", "corn", "paneer", "capsicum"]),
    ("vinay", ["tomato"]),
]
for person, toppings in orders:
    print(person, "->", end=" ")
    order_summary(*toppings)
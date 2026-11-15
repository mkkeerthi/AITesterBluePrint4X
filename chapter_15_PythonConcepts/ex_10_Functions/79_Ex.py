# 79_Ex.py
# Practical *args example: make_pizza(*toppings) accepts any number of topping
# names per person and prints the collected tuple.
def make_pizza(*toppings):
    print(toppings)


pramod = make_pizza("cheese","corn")
yoga = make_pizza("cheese","corn","paneer","capsicm")
vinay = make_pizza("tomato")
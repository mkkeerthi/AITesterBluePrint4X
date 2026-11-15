# 81_ScopreFn.py
# Compares scopes: the module-level "public_toilet" is visible inside every
# function, while "private_toilet" defined inside home() is local to it.
public_toilet = "PB"


def home():
    private_toilet = "PT"
    print(public_toilet)
    print(private_toilet)

def stranger():
    print(public_toilet)
    # print(private_toilet)


    
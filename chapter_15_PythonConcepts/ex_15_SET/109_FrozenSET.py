# 109_FrozenSET.py
# Frozenset - an immutable set. It is created with frozenset() from a list and
# cannot be modified: calling .add() would raise an AttributeError.
# Frozen Set (Immutable Set)
# A frozenset cannot be changed after creation.
my_list = [1, 2, 3, 3]
fset = frozenset(my_list)
# fset.add(4) AttributeError: 'frozenset' object has no attribute 'add'

print(fset)

# More complex: what a frozenset CAN do (all the read-only set algebra) and
# why hashability matters.
print("union:", fset | {4, 5})
print("intersection:", fset & {2, 3, 9})
print("difference:", fset - {1})

# Frozensets are hashable, so they can be dict keys or elements of a set.
permissions = {
    frozenset({"read"}): "viewer",
    frozenset({"read", "write"}): "editor",
    frozenset({"read", "write", "delete"}): "admin",
}
print(permissions[frozenset({"read", "write"})])

nested = {frozenset({1, 2}), frozenset({2, 3})}
print("set of frozensets:", nested)

# Converting back to a mutable set when changes are needed.
mutable = set(fset)
mutable.add(4)
print("converted and grown:", mutable)

# Attempting to change it raises AttributeError.
try:
    fset.add(4)
except AttributeError as error:
    print("AttributeError:", error)
def a():
    return 0


def b():
    return 2


def double(f):
    def doubled():
        return 2 * f()

    return doubled


lst = []

for i in range(2):
    if i == 0:
        inner = locals()["a"]
    else:
        inner = locals()["b"]

    def metric():
        return double(inner)()

    # metric = double(inner)
    lst.append(metric)

for func in lst:
    print(hex(id(func)))
    print(func.__code__)
    print(func())

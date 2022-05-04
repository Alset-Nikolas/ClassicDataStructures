def inc(tree, i, delta):
    while i < len(tree):
        tree[i] += delta
        i = i | (i + 1)


def init(mass):
    tree = [0 for x in range(len(mass))]
    for i, x in enumerate(mass):
        inc(tree, i, x)
    return tree


def _summa(tree, r):
    res = 0
    while r >= 0:
        res += tree[r]
        r = (r & (r + 1)) - 1
    return res


def summa(tree, l, r):
    return _summa(tree, r) - _summa(tree, l - 1)



if __name__ == '__main__':
    a = [1, 2, 3, 4, 5]
    tree = init(a)
    print(summa(tree, 1, 3))

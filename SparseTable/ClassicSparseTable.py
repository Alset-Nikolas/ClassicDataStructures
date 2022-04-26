import math


def calc_max_stepen_2(n):
    deg = [0, 0]
    for x in range(1, n + 1):
        deg.append(deg[-1])
        # Проверка на степень двойки x & (x-1) == 0, только если x степень 2
        if x & (x - 1) == 0:
            deg[-1] += 1
    return deg


def calc_sparse(mass):
    sparse = []
    sparse.append(mass)

    for k in range(0, math.floor(math.log2(n))):
        sparse.append([0] * n)
        for i in range(n):
            # Как вычислить быстро 2**k -> (1<<k)
            # j = i + 2**k
            j = i + (1 << k)
            if j < n:
                sparse[k + 1][i] = min(sparse[k][i], sparse[k][j])
            else:
                sparse[k + 1][i] = sparse[k][i]
    return sparse


def get_min(l, r, deg):
    # Как вычислить степень двойки, которая не больше <= r-l+1 (calc_max_stepen_2)  -> deg
    k = deg[r - l + 1]
    if r - (1 << k) + 1 >= 0:
        return min(sparse[k][l], sparse[k][r - (1 << k) + 1])
    return sparse[k][l]


if __name__ == '__main__':
    mass = [0, 1, 2, 2, 2, 2, -1, 2, 3, 4, 5, 0, -100, 100, -200, 10]
    n = len(mass)
    sparse = calc_sparse(mass)
    deg = calc_max_stepen_2(n)
    ans = get_min(1, 2, deg)
    print(ans)

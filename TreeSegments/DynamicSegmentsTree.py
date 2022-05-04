class Node:
    def __init__(self, val, lx, rx):
        self.val = val
        self.lx = lx
        self.rx = rx
        self.l_child = None
        self.r_child = None

    def __str__(self):
        return f"{self.val}"


class DynamicTree:
    def __init__(self, n):
        self.N_max = n
        self.mass_n = 0
        self.root = None
        self.nodes = []

    def create(self):
        self.root = Node(val=0, lx=0, rx=self.N_max)
        self.nodes.append(self.root)
        return self.root

    def update(self, pos, v, delta):
        self.nodes[v].val += delta
        if self.nodes[v].rx - self.nodes[v].lx == 1:
            return
        m = (self.nodes[v].lx + self.nodes[v].rx + 1) >> 1
        # Создание левого сына
        if self.nodes[v].l_child is None and pos < m:
            self.nodes.append(Node(val=0, lx=self.nodes[v].lx, rx=m))
            self.nodes[v].l_child = len(self.nodes) - 1
        # Спуск в левого сына
        if pos < m:
            self.update(pos, self.nodes[v].l_child, delta)

        if pos >= m:
            if self.nodes[v].r_child is None:
                self.nodes.append(Node(val=0, lx=m, rx=self.nodes[v].rx))
                self.nodes[v].r_child = len(self.nodes) - 1
            self.update(pos, self.nodes[v].r_child, delta)

    def summa(self, l, r, v=None):
        v = v or 0
        ans = 0
        if l <= self.nodes[v].lx and self.nodes[v].rx <= r:
            return self.nodes[v].val

        if self.nodes[v].l_child is not None and self.nodes[v].lx<r:
            ans += self.summa(l, r, self.nodes[v].l_child)
        if self.nodes[v].r_child is not None and self.nodes[v].rx>l:
            ans += self.summa(l, r, self.nodes[v].r_child)
        return ans

    def set(self, i, delta):
        self.update(pos=i, v=0, delta=delta)

    def __str__(self):
        return " ".join([str(x) for x in self.nodes])


def check():
    '''Проверить корректность структуры'''
    import random
    import datetime
    now_time = datetime.datetime.now()
    end_time = now_time + datetime.timedelta(seconds=15)
    n_max = 10 ** 18
    while datetime.datetime.now() < end_time:
        a = [random.randint(1, 10000) for x in range(random.randint(1, 1000))]
        tree = DynamicTree(n_max)
        tree.create()
        for i in range(len(a)):
            x = a[i]
            tree.set(i, x)
        start = 0
        while start < 20:
            l = random.randint(0, len(a))
            r = random.randint(l, len(a))
            if sum(a[l:r]) != tree.summa(l, r):
                print(f"Ошибка при a={a}\tl={l}\tr={r}")
                print(f"suuma_real={sum(a[l:r])}")
                print(f"Через дерево {tree.sum(l, r)}")
                exit()
            start += 1
    print("Все тесты прошли успешно! :)")

if __name__ == '__main__':
    n_max = 10 ** 18
    tree = DynamicTree(n_max)
    root = tree.create()
    mass = [1, 1, 5]
    for i in range(len(mass)):
        x = mass[i]
        tree.set(i, x)

    print(tree.summa(1,3))
    # check()



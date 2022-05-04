class ClassicTreeFenwick:
    def __init__(self, mass):
        self.mass = mass
        self.n_mass = len(self.mass)
        self.tree = [0 for _ in range(self.n_mass)]
        self.si = [0 for _ in range(self.n_mass)]

    def create(self):
        for i in range(self.n_mass):
            self.update(pos=i, val=self.mass[i])

    def update(self, pos, val):
        def g(i):
            return i | (i + 1)
        start_i = pos
        while start_i < self.n_mass:
            self.si[start_i] += val
            start_i = g(start_i)

    def pref_sum(self, r):
        def f(i):
            return i & (i+1)
        res = 0
        end_i = r
        while end_i >= 0:
            res += self.si[end_i]
            end_i = f(end_i) - 1
        return res

    def sum(self, l, r):
        return self.pref_sum(r) - self.pref_sum(l-1)

def check():
    '''Проверить корректность структуры'''
    import random
    import datetime
    now_time = datetime.datetime.now()
    end_time = now_time + datetime.timedelta(seconds=15)
    while datetime.datetime.now() < end_time:
        a = [random.randint(1, 10000) for x in range(random.randint(1, 1000))]
        tree = ClassicTreeFenwick(a)
        tree.create()
        start = 0
        while start < 20:
            l = random.randint(0, len(a)-1)
            r = random.randint(l, len(a)-1)
            if sum(a[l:r+1]) != tree.sum(l, r):
                print(f"l={l}, r={r+1}")
                print(f"Ошибка при a={a}\tl={l}\tr={r}")
                print(f"suuma_real={sum(a[l:r-1])}")
                print(f"Через дерево {tree.sum(l, r)}")
                exit()
            start += 1
    print("Все тесты прошли успешно! :)")

if __name__ == '__main__':
    mass = [1, 2, 3, 4, 5]
    tree = ClassicTreeFenwick(mass)
    tree.create()
    print(tree.sum(0, 1))
    check()
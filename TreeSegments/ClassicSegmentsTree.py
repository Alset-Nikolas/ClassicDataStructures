import math


class ClassicSegmentsTree:
    def __init__(self, mass):
        self.mass = mass.copy()
        self.mass_n = len(self.mass)
        self.last_line_n = math.ceil(math.log2(self.mass_n))
        self.tree = [0 for _ in range(sum([1 << x for x in range(self.last_line_n + 1)]))]
        self.n = len(self.tree)

    def create(self):
        '''Заполнить Структуру 0(N*log(N))'''
        self.mass_update()
        for i, val in enumerate(self.mass):
            self.set(i, val)

    def mass_update(self):
        '''Дозаполним массив нейтральными элементами, для красивого дерева O(C)'''
        new_len_mass = 1 << self.last_line_n
        if self.mass_n != new_len_mass:
            self.mass += [0] * (new_len_mass - self.mass_n)
            self.mass_n = new_len_mass

    def set(self, i, v, x=0, lx=0, rx=None):
        '''
        Поменять значение mass[i] = v  ~ O(log(n))
        :param i:  index mass
        :param v: value
        :param x: Вершина рассмотрения
        :param lx:  Левый предел соответ. вершине x
        :param rx:  Правый предел соответ. верщине x
        :return: None
        '''
        rx = rx or self.mass_n
        if rx - lx == 1:
            self.tree[x] = v
            return
        m = (rx + lx) >> 1
        if i < m:
            self.set(i, v, 2 * x + 1, lx, m)
        else:
            self.set(i, v, 2 * x + 2, m, rx)
        # TODO в общ сл-е нужно вернуть результат (a o b) o c == a o (b o c) функции
        self.tree[x] = self.tree[2 * x + 1] + self.tree[2 * x + 2]

    def sum(self, l, r, x=0, lx=0, rx=None):
        '''
        Посчитать сумму на отрезке  ~ O(log(n))
        :param l: Индекс левой границы массива A
        :param r: Индекс равой границы массива A
        :param x: Индекс вершины поддерва
        :param lx: Левый предел соответ. вершине x
        :param rx: Правый предел соответ. верщине x
        :return:
        '''
        rx = rx or self.mass_n
        if l <= lx and r >= rx:
            # Случ: [l [lx, rx] r]
            return self.tree[x]
        if l >= rx or r <= lx:
            # Случ:  [lx, rx] [l , r] or [l , r] [lx, rx]
            # TODO в общ сл-е нужно вернуть нейтральный элемент
            return 0
        m = (lx + rx) >> 1
        sl = self.sum(l, r, 2 * x + 1, lx, m)
        sr = self.sum(l, r, 2 * x + 2, m, rx)
        # TODO в общ сл-е нужно вернуть результат (a o b) o c == a o (b o c) функции
        return sl + sr

    def __str__(self):
        return f"{self.tree}"


def check():
    '''Проверить корректность структуры'''
    import random
    import datetime
    now_time = datetime.datetime.now()
    end_time = now_time + datetime.timedelta(seconds=15)
    while datetime.datetime.now() < end_time:
        a = [random.randint(1, 10000) for x in range(random.randint(1, 1000))]
        tree = ClassicSegmentsTree(a)
        tree.create()
        start = 0
        while start < 20:
            l = random.randint(0, len(a))
            r = random.randint(l, len(a))
            if sum(a[l:r]) != tree.sum(l, r):
                print(f"Ошибка при a={a}\tl={l}\tr={r}")
                print(f"suuma_real={sum(a[l:r])}")
                print(f"Через дерево {tree.sum(l, r)}")
                exit()
            start += 1
    print("Все тесты прошли успешно! :)")


if __name__ == '__main__':
    A = [5, 2, 6, 7, 8, 4, 4, 6, 7]
    tree = ClassicSegmentsTree(A)
    tree.create()
    sum_ = tree.sum(0, 2)
    print(sum_)

    check()

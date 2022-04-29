# Кол-во чисел на отрезке, значения которых лежат в отрезке [x, y]
# Есть статический мас A=a0, a1, an-1
# Запрос с l-го числа по r число узнать кол-во чисел, которые  x<=a_i<=y
# func(l,r,x,y) -> k
# С помощью таких запросов можно находить кол-во различных чисел на отрезке

# Кол-во чисел принадлеж [x, y]==(кол-во чисел >= x) - (кол-во чисел >= y + 1)
# Для этого нужно дерево MergeSort / Fractional Coscading
# Идея построить Дерево MergeSort и это будет дерево отрезков,
# В нем с помощью бин поиска ищем ответ


import math
class ClassicSegmentsTree:
    def __init__(self, mass):
        self.mass = mass.copy()
        self.mass_n = len(self.mass)
        self.last_line_n = math.ceil(math.log2(self.mass_n))
        self.tree = [[] for _ in range(sum([1 << x for x in range(self.last_line_n + 1)]))]
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
            self.mass += [] * (new_len_mass - self.mass_n)
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
            self.tree[x] = [v]
            return
        m = (rx + lx) >> 1
        if i < m:
            self.set(i, v, 2 * x + 1, lx, m)
        else:
            self.set(i, v, 2 * x + 2, m, rx)
        # Поменял как слияние двух массивов
        self.tree[x] = self.merge(self.tree[2 * x + 1], self.tree[2 * x + 2])

    def merge(self, list1, list2):
        i = 0
        j = 0
        ans = []
        while i < len(list1) and j < len(list2):
            if list1[i] < list2[j]:
                ans.append(list1[i])
                i += 1
            else:
                ans.append(list2[j])
                j += 1
        while i < len(list1):
            ans.append(list1[i])
            i += 1
        while j < len(list2):
            ans.append(list2[j])
            j += 1
        return ans

    def calk_k(self, mass, porog):
        l = 0
        r = len(mass)
        while r > l:
            m = (r + l) >> 1
            if mass[m] >= porog:
                r = m
            else:
                l = m + 1
        return len(mass) - l

    def get_k(self, l, r, x=0, lx=0, rx=None, porog=0):
        '''
        Посчитать кол-ва чисел на отрезке >= porog  ~ O(log^2(n))
        :param l: Индекс левой границы массива A
        :param r: Индекс равой границы массива A
        :param x: Индекс вершины поддерва
        :param lx: Левый предел соответ. вершине x
        :param rx: Правый предел соответ. верщине x
        :param porog: значение сравнения
        :return:
        '''
        rx = rx or self.mass_n
        # print(f"l={l} r={r} lx={lx} rx={rx} porog={porog} x={x}")
        if l <= lx and r >= rx:
            # Случ: [l [lx, rx] r]
            return self.calk_k(self.tree[x], porog)
        if l >= rx or r <= lx:
            # Случ:  [lx, rx] [l , r] or [l , r] [lx, rx]
            return 0
        m = (lx + rx) >> 1
        sl = self.get_k(l, r, 2 * x + 1, lx, m, porog)
        sr = self.get_k(l, r, 2 * x + 2, m, rx, porog)
        # TODO в общ сл-е нужно вернуть результат (a o b) o c == a o (b o c) функции
        return sl + sr

    def __str__(self):
        return f"{self.tree}"


def calc_ans(tree, l, r, x, y):
    '''[x, y]==(кол-во чисел >= x) - (кол-во чисел >= y + 1)'''
    more_x = tree.get_k(l=l, r=r, porog=x)
    more_y = tree.get_k(l=l, r=r, porog=y + 1)
    return more_x - more_y


def check():
    '''Проверка реализации'''
    import random
    import datetime

    def long_func(l, r, mass, porog):
        ans = 0
        for x in mass[l:r]:
            if x >= porog:
                ans += 1
        return ans

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
            porog = random.randint(0, r)
            if tree.get_k(l=l, r=r, porog=porog) != long_func(l, r, a, porog):
                print(f"Ошибка при a={a}\tl={l}\tr={r}")
                print(f"suuma_real={sum(a[l:r])}")
                print(f"Через дерево {tree.get_k(l, r)}")
                exit()
            start += 1
    print("Все тесты прошли успешно! 1/2 :)")


def test_go():
    check()
    import random
    import datetime
    def long_func(mass, l, r, x, y):
        ans = 0
        for v in mass[l:r]:
            if x <= v <= y:
                ans += 1
        return ans

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
            x = random.randint(min(a) - 1, max(a) + 1)
            y = random.randint(x, max(a) + 1)
            if calc_ans(tree, l, r, x, y) != long_func(a, l, r, x, y):
                print(f"Ошибка при a={a}\tl={l}\tr={r}")
                print(f"suuma_real={long_func(a, l, r, x, y)}")
                print(f"Через дерево {calc_ans(tree, l, r, x, y)}")
                exit()
            start += 1
    print("Все тесты прошли успешно! 2/2 :)")


if __name__ == '__main__':
    A = [5, 2, 6, 7, 8, 4, 4, 6, 7]
    l = 1
    r = 8
    x = 3
    y = 4
    tree = ClassicSegmentsTree(A)
    tree.create()
    ans = calc_ans(tree, l, r, x, y)
    print(ans)
    test_go()

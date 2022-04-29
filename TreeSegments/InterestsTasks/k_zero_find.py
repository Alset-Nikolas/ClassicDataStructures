# Задача:
# K-ый ноль на отрезке
# есть mass =[a0, a1, a2, .. ,an-1] - из 0/1
# Есть несколько типов запросов
#       1. update в точке a[pos] = val
#       2. c l-ый по r-ый элемент нужно найти k-ый ноль [l, r] --> k0
# Теперь будем хранить кол-во нулей на отрезке


#                 6
#         4               2
#     2      2        1       1
#   1   1   1   1   0   0   1   1
#   |   |   |   |   |   |   |   |
#   0   0   0   0   1   1   0   0
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


def go(v, k, tree):
    if v * 2 + 1 >= len(tree):
        if tree[v] == k:
            return v
        else:
            return -1
    if k > tree[2 * v + 1]:
        return go(2 * v + 2, k - tree[2 * v + 1], tree_list)
    if tree[2 * v + 1] >= k:
        return go(2 * v + 1, k, tree)


def negative(mass):
    for i in range(len(mass)):
        if mass[i] == 0:
            mass[i] = 1
        else:
            mass[i] = 0


def find_index(k, l, r):
    m = tree.sum(l=0, r=l)
    new_k = k + m
    p = go(0, new_k, tree_list)
    if p == -1:
        print("Нет такого")
    else:
        ans_i = p - (n - 1)
        if ans_i <= r:
            print("Ответ=", ans_i)
            return ans_i
        else:
            print("Нет такого")
    return None


if __name__ == '__main__':
    mass = [0, 0, 0, 0, 1, 1, 0, 0]
    print(f"mass={mass}")
    k = 2
    l = 4
    r = 8
    negative(mass)

    print(f"mass_neg={mass}")
    tree = ClassicSegmentsTree(mass)
    tree.create()
    tree_list = tree.tree
    n = tree.mass_n

    ans_i = find_index(k, l, r)
    tree.set(i=0, v=int(not bool(mass[0])))
    print(f"mass[0] change -> mass_neg={tree_list[n - 1:]}")
    ans_i = find_index(k, l, r)

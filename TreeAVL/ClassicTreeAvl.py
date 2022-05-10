import math

from ClassicBinaryTree import ClassicBinaryTree


class ClassicTreeAvl(ClassicBinaryTree):
    def __init__(self):
        super(ClassicTreeAvl, self).__init__()

    def rotate_left(self, node_p):
        '''
        Малый левый поворот
        '''

        if node_p.r is None:
            return

        # Запоминаем детей узла node_q
        main_parent = node_p.parent
        node_q = node_p.r
        a = node_p.l
        b = node_q.l
        c = node_q.r

        # Меняем ссылки node_q
        node_q.parent = main_parent
        node_q.r = c
        if c:
            c.parent = node_q
        node_q.l = node_p

        # Меняем ссылки node_p
        node_p.r = b
        if b:
            b.parent = node_p
        node_p.l = a
        if a:
            a.parent = node_p
        node_p.parent = node_q

        self.upgrate_h(node_p)
        self.upgrate_h(node_q)
        if main_parent is None:
            self.root = node_q
            self.upgrate_h(self.root)
        else:
            if self.compare_to_parent(node_q):
                main_parent.r = node_q
            else:
                main_parent.l = node_q
            self.upgrate_h(main_parent)

    def rotate_right(self, node_q):
        '''
           Малый правый поворот
        '''
        node_p = node_q.l

        if node_p is None:
            return
        main_parent = node_q.parent

        a = node_p.l
        b = node_p.r
        c = node_q.r
        # Меняем ссылки node_q
        node_q.r = c
        if c:
            c.parent = node_q
        node_q.l = b
        if b:
            b.parent = node_q
        node_q.parent = node_p

        # Меняем ссылки node_p
        node_p.parent = main_parent
        node_p.r = node_q
        node_p.l = a
        if a:
            a.parent = node_p

        self.upgrate_h(node_q)
        self.upgrate_h(node_p)
        if main_parent is None:
            self.root = node_p
            self.upgrate_h(self.root)
        else:
            if self.compare_to_parent(node_p):
                main_parent.r = node_p
            else:
                main_parent.l = node_p
            self.upgrate_h(main_parent)

    def big_rotate_left(self, node_x):
        node_y = node_x.r
        if node_y is not None:
            self.rotate_right(node_y)
        self.rotate_left(node_x)

    def big_rotate_right(self, node_x):
        node_y = node_x.l
        if node_y is not None:
            self.rotate_left(node_y)
        self.rotate_right(node_x)

    def balance(self, node_x):
        super(ClassicTreeAvl, self).balance(node_x)
        if node_x.diff == -2:
            # высота правого поддерева на 2 меньше чем левого
            left_child = node_x.l
            if left_child.diff <= 0:
                self.rotate_right(node_x)
            else:
                self.big_rotate_right(node_x)
        if node_x.diff == 2:
            # высота правого поддерева на 2 больше чем левого
            right_child = node_x.r
            if right_child.diff >= 0:
                self.rotate_left(node_x)
            else:
                self.big_rotate_left(node_x)


def create_mass(n_max):
    a = []
    while len(a) != n_max:
        # Создаем разные n_max числа
        new_val = random.randint(1, 10000)
        a.append(new_val)
        a = list(set(a))
    return a


def pprint(n_list, h_list):
    fig = plt.figure()
    graph1 = plt.plot(n_list, h_list[1:], label='Опыт')
    plt.plot(n_list, [1.45 * math.log2(n_i + 2) for n_i in n_list], label='Теория (max)')
    plt.plot(n_list, [math.log2(n_i) for n_i in n_list], label='log2(n)')
    plt.title("Высота дерева, mass=[случайной последовательности]")
    plt.xlabel("Кол-во чисел в mass, n")
    plt.ylabel("H(n)")

    plt.legend()
    plt.show()


def check():
    '''Проверить корректность структуры'''

    n_max = 100  # Длина массива
    m = 1000  # Кол-во опытов
    h = [0 for _ in range(n_max + 1)]  # H_max
    print('Пару секунд :) Идет долгая проверка')
    for _ in range(m):
        print(f'{_}/{m - 1}')
        tree = ClassicTreeAvl()
        a = create_mass(n_max=n_max)

        for i, x in enumerate(a):
            # Заполняеи дерево и считаем высоту
            # (ПРОВЕРКА ВСТАВКИ)
            tree.insert(x)
            n_i = i + 1
            h[n_i] += tree.root.h
        h[len(a)] += tree.root.h
        while len(a) != 0:
            # Удаляем в случайном порядке числа и считаем дерево
            # (ПРОВЕРКА УДАЛЕНИЯ)
            i = random.randint(0, len(a) - 1)
            new_val = a.pop(i)
            tree.extract(new_val)
            if tree.root is None:
                h[len(a)] += 0
            else:
                h[len(a)] += tree.root.h

    h = [h_i / (2 * m) for h_i in h]  # Нормируем
    n = range(1, n_max + 1)

    pprint(n, h)

    print("Все тесты прошли успешно! :)")


if __name__ == '__main__':
    import random
    import matplotlib.pyplot as plt

    check()

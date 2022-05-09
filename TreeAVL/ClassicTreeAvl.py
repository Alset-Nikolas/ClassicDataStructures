import math

from ClassicBinaryTree import ClassicBinaryTree


class ClassicTreeAvl(ClassicBinaryTree):
    def __init__(self):
        super(ClassicTreeAvl, self).__init__()

    def rotate_left(self, node_p):
        '''
        Малый левый поворот
        '''
        print('rotate_left p = ', node_p )


        if node_p.r is None:
            return

        # Запоминаем детей узла node_q
        main_parent = node_p.parent
        node_q = node_p.r
        print('Было')
        if main_parent:
            print(f'main_parent={main_parent} l={main_parent.l} r={main_parent.r} p={main_parent.parent}')
        print(f'node_q={node_q} l={node_q.l} r={node_q.r} p={node_q.parent}')
        print(f'node_p={node_p} l={node_p.l} r={node_p.r} p={node_p.parent}')
        a = node_p.l
        b = node_q.l
        c = node_q.r
        # Меняем ссылки node_q

        node_q.parent = main_parent
        node_q.r = c
        node_q.l = node_p

        # Меняем ссылки node_p
        node_p.r = b
        node_p.l = a
        node_p.parent = node_q

        self.upgrate_h(node_p)
        self.upgrate_h(node_q)
        if main_parent is None:
            self.root = node_q
            self.upgrate_h(self.root)
        else:
            print('self.compare_to_parent(node_q)', self.compare_to_parent(node_q))
            if self.compare_to_parent(node_q):
                main_parent.r = node_q
            else:
                main_parent.l = node_q
            self.upgrate_h(main_parent)
        print('Стало')
        print(f'node_q={node_q} l={node_q.l} r={node_q.r} p={node_q.parent}')
        print(f'node_p={node_p} l={node_p.l} r={node_p.r} p={node_p.parent}')
        if main_parent:
            print(f'main_parent={main_parent} l={main_parent.l} r={main_parent.r} p={main_parent.parent}')


    def rotate_right(self, node_q):
        '''
           Малый правый поворот
        '''
        print('rotate_right q=', node_q)
        node_p = node_q.l
        print('Было')

        print(f'node_q={node_q} l={node_q.l} r={node_q.r} p={node_q.parent}')
        print(f'node_p={node_p} l={node_p.l} r={node_p.r} p={node_p.parent}')
        if node_p is None:
            return
        main_parent = node_q.parent
        if main_parent:
            print(f'main_parent={main_parent} l={main_parent.l} r={main_parent.r} p={main_parent.parent}')
        a = node_p.l
        b = node_p.r
        c = node_q.r
        # Меняем ссылки node_q
        node_q.r = c
        node_q.l = b
        node_q.parent = node_p

        # Меняем ссылки node_p
        node_p.parent = main_parent
        node_p.r = node_q
        node_p.l = a

        self.upgrate_h(node_q)
        self.upgrate_h(node_p)
        if main_parent is None:
            self.root = node_p
            self.upgrate_h( self.root)
        else:
            print('self.compare_to_parent(node_p)', self.compare_to_parent(node_p))
            if self.compare_to_parent(node_p):
                main_parent.r = node_p
            else:
                main_parent.l = node_p
            self.upgrate_h(main_parent)
            print(f'main_parent={main_parent} l={main_parent.l} r={main_parent.r} p={main_parent.parent}')
        print('Стало')
        print(f'node_q={node_q} l={node_q.l} r={node_q.r} p={node_q.parent}')
        print(f'node_p={node_p} l={node_p.l} r={node_p.r} p={node_p.parent}')


    def big_rotate_left(self, node_x):
        print('big_rotate_left', node_x)
        node_y = node_x.r
        if node_y is not None:
            self.rotate_right(node_y)
        self.rotate_left(node_x)

    def big_rotate_right(self, node_x):
        print('big_rotate_right')
        node_y = node_x.l

        if node_y is not None:
            self.rotate_left(node_y)
        self.rotate_right(node_x)


    def balance(self, node_x):
        super(ClassicTreeAvl, self).balance(node_x)
        print('balance', node_x, node_x.diff)
        if node_x.diff == -2:
            #высота правого поддерева на 2 меньше чем левого
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
        print()
        print('v'*10)
        print('='*10)
        print(self)
        print('='*10)
        print('^'*10)



def check():
    '''Проверить корректность структуры'''
    import random
    import datetime
    import matplotlib.pyplot as plt
    n = range(1, 100)
    m = 1000
    h = [0 for _ in n]

    for n_i in n:
        print(n_i)
        h_mid = 0
        for m_j in range(m):
            tree = ClassicBinaryTree()
            for x in range(n_i):
                new_val = random.randint(-10000, 10000)
                tree.insert(new_val)
            h_mid += tree.root.h
        h[n_i-1] = h_mid//m
    fig = plt.figure()
    graph1 = plt.plot(n, h)
    plt.plot(n, [math.log(n_i, (5**(0.5)+1)/2) for n_i in n])
    plt.show()

    print("Все тесты прошли успешно! :)")

check()

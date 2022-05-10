import math

from ClassicBinaryTree import ClassicBinaryTree


class ClassicTreeAvl(ClassicBinaryTree):
    def __init__(self):
        super(ClassicTreeAvl, self).__init__()

    def rotate_left(self, node_p):
        '''
        Малый левый поворот
        '''
        # print('rotate_left p = ', node_p )


        if node_p.r is None:
            return

        # Запоминаем детей узла node_q
        main_parent = node_p.parent
        node_q = node_p.r
        # print('Было')
        # if main_parent:
        #     print(f'main_parent={main_parent} l={main_parent.l} r={main_parent.r} p={main_parent.parent}')
        # print(f'node_q={node_q} l={node_q.l} r={node_q.r} p={node_q.parent}')
        # print(f'node_p={node_p} l={node_p.l} r={node_p.r} p={node_p.parent}')
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
            # print('self.compare_to_parent(node_q)', self.compare_to_parent(node_q))
            if self.compare_to_parent(node_q):
                main_parent.r = node_q
            else:
                main_parent.l = node_q
            self.upgrate_h(main_parent)
        # print('Стало')
        # print(f'node_q={node_q} l={node_q.l} r={node_q.r} p={node_q.parent}')
        # print(f'node_p={node_p} l={node_p.l} r={node_p.r} p={node_p.parent}')
        # if main_parent:
        #     print(f'main_parent={main_parent} l={main_parent.l} r={main_parent.r} p={main_parent.parent}')


    def rotate_right(self, node_q):
        '''
           Малый правый поворот
        '''
        # print('rotate_right q=', node_q)
        node_p = node_q.l
        # print('Было')
        #
        # print(f'node_q={node_q} l={node_q.l} r={node_q.r} p={node_q.parent}')
        # print(f'node_p={node_p} l={node_p.l} r={node_p.r} p={node_p.parent}')
        if node_p is None:
            return
        main_parent = node_q.parent
        # if main_parent:
        #     print(f'main_parent={main_parent} l={main_parent.l} r={main_parent.r} p={main_parent.parent}')
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
            # print('self.compare_to_parent(node_p)', self.compare_to_parent(node_p))
            if self.compare_to_parent(node_p):
                main_parent.r = node_p
            else:
                main_parent.l = node_p
            self.upgrate_h(main_parent)
        #     print(f'main_parent={main_parent} l={main_parent.l} r={main_parent.r} p={main_parent.parent}')
        # print('Стало')
        # print(f'node_q={node_q} l={node_q.l} r={node_q.r} p={node_q.parent}')
        # print(f'node_p={node_p} l={node_p.l} r={node_p.r} p={node_p.parent}')


    def big_rotate_left(self, node_x):
        # print('big_rotate_left', node_x)
        node_y = node_x.r
        if node_y is not None:
            self.rotate_right(node_y)
        self.rotate_left(node_x)

    def big_rotate_right(self, node_x):
        # print('big_rotate_right')
        node_y = node_x.l

        if node_y is not None:
            self.rotate_left(node_y)
        self.rotate_right(node_x)


    def balance(self, node_x):
        super(ClassicTreeAvl, self).balance(node_x)
        # print('balance', node_x, node_x.diff)
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
        # print()
        # print('v'*10)
        # print('='*10)
        # print(self)
        # print('='*10)
        # print('^'*10)



def check():
    '''Проверить корректность структуры'''
    import random
    import matplotlib.pyplot as plt
    n_max = 10
    m = 1000
    h = [0 for _ in range(n_max+1)]
    for _ in range(m):
        print(_)
        tree = ClassicTreeAvl()
        a = []
        while len(a) != n_max:
            new_val = random.randint(1, 10000)
            a.append(new_val)
            a = list(set(a))

        for i, x in enumerate(a):
            tree.insert(x)
            n_i = i + 1
            h[n_i] += tree.root.h



    h = [h_i/m for h_i in h]
    n = range(1, n_max+1)
    print(h[1:])

    fig = plt.figure()
    graph1 = plt.plot(n, h[1:], label='Опыт')
    plt.plot(n, [1.45*math.log2(n_i+2) for n_i in n], label='Теория (max)')
    plt.plot(n, [math.log2(n_i) for n_i in n], label='log2(n)')
    plt.title("Высота дерева, mass=[случайной последовательности]")
    plt.xlabel("Кол-во чисел в mass, n")
    plt.ylabel("H(n)")

    plt.legend()
    plt.show()

    print("Все тесты прошли успешно! :)")

def check2():
    '''Проверить корректность структуры'''
    import random
    import matplotlib.pyplot as plt
    n_max = 5
    m = 1000
    h = [0 for _ in range(n_max+1)]
    h_del = [0 for _ in range(n_max+1)]
    for _ in range(m):
        print(_)
        tree = ClassicTreeAvl()
        a = []
        while len(a) != n_max:
            new_val = random.randint(1, 10000)
            a.append(new_val)
            a = list(set(a))

        for i, x in enumerate(a):
            tree.insert(x)
            n_i = i + 1
            h[n_i] += tree.root.h
        h_del[len(a)] = tree.root.h
        # print('Правильное дерево')
        # print(tree)
        # print()
        while len(a) != 0:
            i = random.randint(0, len(a) - 1)
            print(i, len(a), a)
            new_val = a.pop(i)
            # print('Удаляем значение new_val=', new_val)
            # try:
            tree.extract(new_val)
            #     print('tree.n', tree.n)
            # except:
            #     print('Пытались удалить new_val', new_val)
            #     print(tree)
            #     print(tree.root)
            #     exit()
            if tree.root is None:
                h_del[len(a)] += 0
            else:
                h_del[len(a)] += tree.root.h
            # print(tree)
            # input()
            # print()


    h_del = [h_i/m for h_i in h]
    n = range(1, n_max+1)


    fig = plt.figure()
    graph1 = plt.plot(n, h_del[1:], label='Опыт')
    plt.plot(n, [1.45*math.log2(n_i+2) for n_i in n], label='Теория (max)')
    plt.plot(n, [math.log2(n_i) for n_i in n], label='log2(n)')
    plt.title("Высота дерева, mass=[случайной последовательности]")
    plt.xlabel("Кол-во чисел в mass, n")
    plt.ylabel("H(n)")

    plt.legend()
    plt.show()

    print("Все тесты прошли успешно! :)")

check2()
import random
a = [3296, 814, 6258, 4247, 7993]
tree = ClassicTreeAvl()
for x in a:
    tree.insert(x)
print(tree)
tree.extract(3296)
print(tree)
# index_pop = []
# while len(a) != 0:
#     i = random.randint(0, len(a) - 1)
#     print(i, len(a))
#     new_val = a.pop(i)
#     tree.extract(new_val)
# tree.extract(3711)
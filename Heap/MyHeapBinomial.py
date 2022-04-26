import copy
import math


class BinomialTreeElement:
    def __init__(self, val, key, parent):
        self.val = val
        self.key = key
        self.child_left = None
        self.sibling = None
        self.parent = parent

    '''Происхдит сравнение по ключу'''

    def __ge__(self, other):
        '''>='''
        return self.key >= other.key

    def __le__(self, other):
        '''<='''
        return self.key <= other.key

    def __gt__(self, other):
        '''>'''
        return self.key > other.key

    def __lt__(self, other):
        '''<'''
        return self.key < other.key

    def __str__(self):
        if self.parent is None:
            return f"key = {self.key} parent=NONE"
        return f"key = {self.key} parent={self.parent.key}"


class BinomialTree:
    '''
        Биноминальное дерево, 2**k элементов
    '''

    def __init__(self, k=0):
        self.tree_size = 0
        self.tree_list = []
        self.k = k



    def combinations(self, k, i):
        return math.factorial(i) // (math.factorial(k - i) * math.factorial(i))

    def create(self, mass):
        self.tree_size = len(mass)
        if self.tree_size != 2 ** self.k:
            raise f"Кол-во элементов в дереве != 2**k {self.tree_size}!= {2 ** self.k}"
        self.create_element(mass)
        self.build_tree()

    def create_element(self, mass, k_i=0, first_index=0):
        '''
        Создать элемент дерева
        mass = [(val1, key1), (val2, key2)]
        '''
        if k_i == 0:
            self.tree_list.append(BinomialTreeElement(val=mass[first_index][0], key=mass[first_index][1], parent=None))
            self.create_element(mass, k_i + 1, first_index + 1)
            return
        if k_i > self.k:
            return
        copy_tree = copy.deepcopy(self.tree_list)
        for i in range(len(copy_tree)):
            copy_tree[i].val = mass[first_index][0]
            copy_tree[i].key = mass[first_index][1]
            first_index += 1
        root = copy_tree[0]
        main_root = self.tree_list[0]
        root.parent = main_root
        sister = main_root.child_left
        root.sibling = sister
        main_root.child_left = root
        self.tree_list += copy_tree
        self.create_element(mass, k_i + 1, first_index)

    def __str__(self):
        t = []
        for x in self.tree_list:
            t.append(str(x))
        return f"Tk={self.k}:\n" + "\n".join(t)

    def is_exist(self, i):
        return 0 <= i <= self.tree_size

    def shift_up(self, i, bin_el):
        parent = bin_el.parent
        if parent is not None:
            if parent > bin_el:
                self.change(parent, bin_el)
                self.shift_up(i, parent)

    def change(self, bin_el1, bin_el2):
        bin_el1.key, bin_el2.key = bin_el2.key, bin_el1.key
        bin_el1.val, bin_el2.val = bin_el2.val, bin_el1.val

    def shift_down(self, bin_el):
        child = bin_el.child_left
        min_child = bin_el.child_left
        while child is not None:
            child = child.sibling
            if child is None:
                break
            if min_child > child:
                min_child = child
        if min_child is not None and min_child < bin_el:
            self.change(min_child, bin_el)
            self.shift_down(min_child)

    def build_tree(self):
        for i in range(self.tree_size - 1, -1, -1):
            bin_el = self.tree_list[i]
            self.shift_up(i, bin_el)

    def get_min(self):
        if self.tree_size > 0:
            return self.tree_list[0].key, self.tree_list[0].val
        return None

    def calc_k_tree(self, len_list):
        n = 0
        while len_list > 1:
            n += 1
            len_list //= 2
        return n

    def pop_min(self):
        new_trees = []
        n = 0
        start_index = 1
        end_index = start_index + 2 ** n

        while start_index < self.tree_size:
            self.tree_list[start_index].parent = None
            self.tree_list[start_index].sibling = None
            new_n = len(self.tree_list[start_index:end_index])
            new_tree = BinomialTree(self.calc_k_tree(new_n))
            new_tree.update_tree(self.tree_list[start_index:end_index])
            new_tree.tree_size = new_n
            new_tree.build_tree()
            new_trees.append(new_tree)
            start_index = end_index
            n += 1
            end_index = start_index + 2 ** n
        return new_trees

    def update_tree(self, trees_element):
        self.tree_list = trees_element
        self.tree_size = len(self.tree_list)
        return self

    def __add__(self, other):
        if self.k != other.k:
            raise f"Порядок деревьев {self.l} {other.k}"
        tree_main = self
        tree = other
        if self.get_min() > tree.get_min():
            tree_main, tree = other, self
        main_root = tree_main.tree_list[0]
        root = tree.tree_list[0]
        root.parent = main_root
        sister = main_root.child_left
        root.sibling = sister
        main_root.child_left = root
        tree_main.tree_list += tree.tree_list
        tree_main.k += 1
        tree_main.tree_size = len(tree_main.tree_list)
        return tree_main


class BinomialHeap:
    '''
    Биномиальная куча
    '''

    def __init__(self):
        self.numbers = None
        self.binomial_trees = []
        self.heap_size = 0


    def create(self, mass):
        self.numbers = mass
        self.heap_size = len(self.numbers)
        n_bin = bin(self.heap_size)[2:]
        start_index = 0
        n_i = 0
        end_index = start_index + 2 ** n_i
        for i, x in enumerate(n_bin[::-1]):
            if x == "1":
                new_tree = BinomialTree(i)
                new_tree.create(self.numbers[start_index:end_index])
                start_index = end_index
                self.binomial_trees.append(new_tree)
            n_i += 1
            end_index = start_index + 2 ** n_i

    def get_min(self):
        min_res = math.inf
        for tree in self.binomial_trees:
            min_i = tree.get_min()
            if min_i < min_res:
                min_res = min_i
        return min_res

    def pop_min(self):
        min_res = math.inf
        min_val = None
        index_tree_min = None
        for i, tree in enumerate(self.binomial_trees):
            min_i, min_val_i = tree.get_min()
            if min_i is not None and min_i < min_res:
                min_val = min_val_i
                min_res = min_i
                index_tree_min = i
        if self.heap_size > 0:
            self.heap_size -= 1
        else:
            raise "Элементы закончились"

        if index_tree_min is not None:
            new_heap = BinomialHeap()
            new_heap.binomial_trees = self.binomial_trees[index_tree_min].pop_min()
            new_heap.heap_size = sum([x.k for x in new_heap.binomial_trees])
            self.binomial_trees.pop(index_tree_min)
            self.binomial_trees = self.merge(new_heap)
        return min_val, min_res

    def merge(self, other):
        '''
        Функция слияния двух куч
        :param other:
        :return: [binominal_trees]
        '''
        first_index = 0
        second_index = 0
        carry = -1
        ans = []
        while first_index < len(self.binomial_trees) and second_index < len(other.binomial_trees):
            tree_1 = self.binomial_trees[first_index]
            tree_2 = other.binomial_trees[second_index]

            if carry == -1:
                if tree_1.k < tree_2.k:
                    ans.append(tree_1)
                    first_index += 1
                elif tree_1.k > tree_2.k:
                    ans.append(tree_2)
                    second_index += 1
                else:
                    carry = tree_1 + tree_2
                    first_index += 1
                    second_index += 1
            else:
                if tree_1.k == tree_2.k:
                    ans.append(carry)
                    carry = tree_1 + tree_2
                    first_index += 1
                    second_index += 1
                elif tree_1.k < tree_2.k and carry.k == tree_1.k:
                    carry = carry + tree_1
                    first_index += 1
                elif tree_2.k < tree_1.k and carry.k == tree_2.k:
                    carry = carry + tree_2
                    second_index += 1
                else:
                    if carry.k != tree_2.k and tree_2.k != tree_1.k and carry.k != tree_1.k:
                        if carry.k < max(tree_2.k, tree_1.k):
                            ans.append(carry)
                            carry = -1
                        elif tree_1.k < max(tree_2.k, carry.k):
                            ans.append(tree_1)
                            first_index += 1
                        else:
                            ans.append(tree_2)
                            second_index += 1
        for index, tree in [(first_index, self.binomial_trees), (second_index, other.binomial_trees)]:
            while index < len(tree):
                tree_1 = tree[index]
                if carry != -1:
                    if carry.k == tree_1.k:
                        carry = tree_1 + carry
                        index += 1
                    elif carry.k > tree_1.k:
                        ans.append(tree_1)
                        index += 1
                    elif carry.k < tree_1.k:
                        ans.append(carry)
                        carry = -1
                else:
                    ans.append(tree_1)
                    index += 1
        if carry != -1:
            ans.append(carry)
        return ans

    def __add__(self, other):
        self.heap_size = self.heap_size + other.heap_size
        self.binomial_trees = self.merge(other)
        return self

    def add(self, new_el):
        new_heap = BinomialHeap()
        new_heap.create([new_el])
        self.heap_size += new_heap.heap_size
        self.binomial_trees = self.merge(new_heap)



def check_sort():
    import random
    start = 0
    print("Поиск неверного варианта")
    while 1:
        numbers = []
        n_st = random.randint(1, 50)
        for i in range(n_st):
            numbers.append((random.randint(-50, 50), random.randint(-50, 50)))

        heap = BinomialHeap()
        heap.create(numbers)
        ans = []
        for x in range(n_st):
            a = heap.pop_min()
            ans.append(a)
        numbers.sort(key=lambda x: x[1])
        if [x[1] for x in ans] != [x[1] for x in numbers]:
            print("Нашел!")
            print(f"Должно быть {[x[1] for x in numbers]}")
            print(f"Получил: {[x[1] for x in ans]}")
            break
        start += 1


def check_merge():
    heap = BinomialHeap()
    heap.create([(1, 1), (2, 2)])
    heap1 = BinomialHeap()
    heap1.create([(1, 1), (2, 2)])
    heap_res = heap + heap1
    for x in range(heap_res.heap_size):
        a = heap.pop_min()
        print(a)


if __name__ == '__main__':
    heap = BinomialHeap()
    heap.create([(1, 1), (2, 2)])
    heap.add((1,0))
    heap.add((3, -1))
    for x in range(heap.heap_size):
        a = heap.pop_min()
        print(a)

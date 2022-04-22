import copy
import math

from HeapBinary import HeapBineryClassic


class BinomialTreeElement:
    def __init__(self, val, key, parent):
        self.val = val
        self.key = key
        self.child_left = None
        self.sibling = None
        self.parent = parent

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
        return f"val={self.val}; key = {self.key}"


class BinomialTree:
    def __init__(self, k):
        self.heap_size = 0
        self.heap_list = []
        self.k = k

    def combinations(self, k, i):
        return math.factorial(i) // (math.factorial(k - i) * math.factorial(i))

    def create_tree(self, mass, k_i=0, first_index=0):
        '''
        mass = [(val1, key1), (val2, key2)]
        '''
        if k_i == 0:
            self.heap_list.append(BinomialTreeElement(val=mass[first_index][0], key=mass[first_index][1], parent=None))
            self.create_tree(mass, k_i + 1, first_index + 1)
            return
        if k_i > self.k:
            return
        copy_tree = copy.deepcopy(self.heap_list)
        for i in range(len(copy_tree)):
            copy_tree[i].val = mass[first_index][0]
            copy_tree[i].key = mass[first_index][1]
            first_index += 1
        root = copy_tree[0]
        main_root = self.heap_list[0]
        root.parent = main_root
        sister = main_root.child_left
        root.sibling = sister
        main_root.child_left = root
        self.heap_list += copy_tree
        self.create_tree(mass, k_i + 1, first_index)

    def __str__(self):
        t = []
        for x in self.heap_list:
            t.append(str(x))
        return "\n".join(t)


bin_ = BinomialTree(3)
bin_.create_tree(mass=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (4, 5), (4, 6), (4, 6)])
print(bin_)

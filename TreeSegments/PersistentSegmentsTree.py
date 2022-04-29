import math


def pprint(node):
    parent = [node]
    ans = []
    while len(parent) > 0:
        nex_parent = []
        ans_i = []
        for p in parent:
            if p is not None:
                ans_i.append(p.value)
                nex_parent.append(p.child_left)
                nex_parent.append(p.child_right)
        parent = nex_parent
        ans.append(ans_i)

    for i in range(len(ans)):
        print(f"{i} : {ans[i]}")


class Node:
    def __init__(self, value, child_left=None, child_right=None):
        self.value = value
        self.child_left = child_left
        self.child_right = child_right

    def __str__(self):
        return f"{self.value}"


class PersistentTree:
    def __init__(self):
        self.roots = []
        self.nodes = []
        self.mass = []
        self.mass_n = 0
        self.i = 0

    def add_root(self):
        start_root = Node(0)
        self.roots.append(start_root)
        return start_root

    def mass_update(self, mass):
        '''Дозаполним массив нейтральными элементами, для красивого дерева O(C)'''
        self.mass = mass.copy()
        self.mass_n = len(self.mass)
        new_len_mass = 1 << math.ceil(math.log2(self.mass_n))
        if self.mass_n != new_len_mass:
            self.mass += [0] * (new_len_mass - self.mass_n)
            self.mass_n = new_len_mass

    def create(self, mass):
        self.mass_update(mass)
        start_root = self.add_root()
        self.build(left=0, right=self.mass_n, x=start_root)

    def new_node(self, value=0):
        node = Node(value)
        self.nodes.append(node)
        return node

    def build(self, left, right, x):
        '''Построение ДО'''
        if right - left == 1:
            x.value = self.mass[left]
            return x.value
        middle = (left + right + 1) >> 1
        x.child_left = self.new_node(0)
        x.child_right = self.new_node(0)
        ls = self.build(left, middle, x.child_left)
        rs = self.build(middle, right, x.child_right)
        x.value = ls + rs
        return ls + rs

    def set(self, i, val, lx, rx, node_x):
        if lx == i and rx == i + 1:
            return self.new_node(val)

        m = (lx + rx + 1) >> 1
        if i < m:
            child_left = self.set(i, val, lx, m, node_x.child_left)
            new_branch = self.new_node()
            new_branch.child_right = node_x.child_right
            new_branch.child_left = child_left
            new_branch.value = new_branch.child_left.value + new_branch.child_right.value
        else:
            child_right = self.set(i, val, m, rx, node_x.child_right)

            new_branch = self.new_node()
            new_branch.child_left = node_x.child_left
            new_branch.child_right = child_right
            new_branch.value = new_branch.child_left.value + new_branch.child_right.value
        return new_branch

    def change(self, i, val):
        root = self.roots[-1]
        new_root = self.set(i, val, lx=0, rx=self.mass_n, node_x=root)
        self.roots.append(new_root)


if __name__ == '__main__':
    a = [1, 2, 3, 4]
    print(f"Дан массив {a}")
    tree = PersistentTree()
    tree.create(a)
    print(f"Дерево start_root={0}:")
    print("=" * 10)
    pprint(tree.roots[0])
    print("="*10)
    print(f"Меняем {0} значение на 5")
    tree.change(i=0, val=5)
    print(f"Дерево root={1}:")
    print("=" * 10)
    pprint(tree.roots[1])
    print("=" * 10)
    print(f"Меняем {1} значение на 5")
    print("=" * 10)
    tree.change(i=1, val=5)
    print("=" * 10)
    pprint(tree.roots[2])
    print("=" * 10)
    print("Смотрим на старые версии ")
    print(f"Дерево start_root={1}:")
    print("=" * 10)
    pprint(tree.roots[1])
    print("=" * 10)
    print(f"Дерево start_root={0}:")
    print("=" * 10)
    pprint(tree.roots[0])
    print("=" * 10)


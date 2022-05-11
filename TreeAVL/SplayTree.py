from ClassicBinaryTree import ClassicBinaryTree, Node


class SplayTree(ClassicBinaryTree):
    def __init__(self):
        self.n = 0
        self.root = None

    def zag(self, node_p):
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
        return node_q

    def zig(self, node_q):
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
        return node_p

    def zig_zig(self, node_x):
        '''До                              После
                           (q)       ->          (x)
                          /   \      ->         /   \
                       (p)     D     ->       A     (p)
                      /   \          ->           /   \
                    (x)    C         ->         B     (q)
                   /   \             ->              /   \
                  A     B            ->            C       D
        :param node_x: Узел x
        :return:
        '''
        p_node = node_x.parent
        q_node = p_node.parent
        self.zig(q_node)
        self.zig(p_node)

    def zag_zag(self, node_x):
        '''До                                   После
                       (q)                             (x)
                      /   \             ->             /   \
                    D     (p)           ->          (p)     D
                        /   \           ->         /   \
                      C     (x)         ->       (q)    C
                           /   \        ->      /   \
                        A       B       ->     A     B
        :param node_x: Узел x
        :return:
        '''
        p_node = node_x.parent
        q_node = p_node.parent
        self.zag(q_node)
        self.zag(p_node)

    def zag_zig(self, node_x):
        '''До
                                    (q)      ->          (x)
                                   /   \     ->          /   \
                                (p)      D   ->       (p)     (q)
                                /   \        ->      /   \   /   \
                              A     (x)      ->     A    B  C    D
                                   /   \
                                B       C
            :param node_x: Узел x
            :return:
        '''
        p_node = node_x.parent
        q_node = p_node.parent
        self.zag(p_node)
        self.zig(q_node)

    def zig_zag(self, node_x):
        '''До
                                    (q)          ->          (x)
                                   /   \         ->          /   \
                                 A     (p)       ->       (q)     (p)
                                      /  \       ->      /   \   /   \
                                   (x)    D      ->     A    B  C    D
                                   /  \
                                  B    C
            :param node_x: Узел x
            :return:
        '''
        p_node = node_x.parent
        q_node = p_node.parent
        self.zig(p_node)
        self.zag(q_node)

    def splay(self, node_x):
        if node_x.parent is None:
            # Если корень, то делать ничего не надо
            return self.root
        parent_x = node_x.parent
        grand_x = parent_x.parent
        if grand_x is None:
            # Если дедушка корень то :
            if self.compare_to_parent(node_x):
                # Если node_x - правый сын parent_x
                self.zag(parent_x)
            else:
                self.zig(parent_x)
            return self.root
            # grand_x - точно не None
        if self.compare_to_parent(node_x) and self.compare_to_parent(parent_x):
            # Если node_x - правый сын parent_x и Если parent_x - правый сын grand_x
            self.zag_zag(node_x)
        elif (not self.compare_to_parent(node_x)) and (not self.compare_to_parent(parent_x)):
            # Если node_x - левый сын parent_x и Если parent_x - левый сын grand_x
            self.zig_zig(node_x)
        elif (self.compare_to_parent(node_x)) and (not self.compare_to_parent(parent_x)):
            # Если node_x - правый сын parent_x и Если parent_x - левый сын grand_x
            self.zag_zig(node_x)
        elif (not self.compare_to_parent(node_x)) and (self.compare_to_parent(parent_x)):
            # Если node_x - правый сын parent_x и Если parent_x - левый сын grand_x
            self.zig_zag(node_x)
        return self.splay(node_x)
    def find(self, find_val: int, node: Node = None):
        '''
        Поиск элемента по значению
        :param find_val: Значение поиска
        :param node: текущий узел
        :param flag_del: Флаг (bool) для удаление узла
        :return: Node - Узел дерева, flag - левая/правая
        '''
        now_node = node or self.root

        if now_node is None:
            return None
        val_node = now_node.val
        if find_val == val_node:
            # усли есть такое значение, то вернет его
            return self.splay(now_node)
        elif find_val < val_node and now_node.l != None:
            return self.find_near_person(find_val, now_node.l)
        elif find_val > val_node and now_node.r != None:
            return self.find_near_person(find_val, now_node.r)
        self.upgrate_h(now_node)
        return None

    def find_near_person(self, find_val: int, node: Node = None):
        '''
        Поиск близкого элемента по значению элемента
        :param find_val: Значение поиска
        :param node: текущий узел
        :param flag_del: Флаг (bool) для удаление узла
        :return: Node - Узел дерева, flag - левая/правая
        '''
        now_node = node or self.root

        if now_node is None:
            return None
        val_node = now_node.val
        if find_val == val_node:
            # усли есть такое значение, то вернет его
            return self.splay(now_node)
        elif find_val < val_node and now_node.l != None:
            return self.find_near_person(find_val, now_node.l)
        elif find_val > val_node and now_node.r != None:
            return self.find_near_person(find_val, now_node.r)
        self.upgrate_h(now_node)
        return self.splay(now_node)

    def set_parent(self, child, parent):
        if child is None:
            return
        child.parent = parent

    def create_tree(self, node_root):
        new_tree = SplayTree()
        if node_root is None:
            return None
        else:
            new_tree.h = node_root.h
            new_tree.root = node_root
            new_tree.n = new_tree.h
            new_tree.root.parent = None
        return new_tree

    def split(self, val):
        root = self.find_near_person(val)
        if root is None:
            # Не нашли такой ключ
            return None, None
        # Делим дерево на 2:
        # левое -> все элементы меньше val
        # правле -> больше или равно val
        if root.val == val:
            left_tree = root.l
            right_tree = root.r
            # Разрезаем
            self.set_parent(child=left_tree, parent=None)
            self.set_parent(child=right_tree, parent=None)
            root.l = None
            root.r = None
            return self.create_tree(left_tree), self.create_tree(right_tree)
        elif root.val < val:
            right_tree = root.r
            root.r = None
            self.set_parent(child=right_tree, parent=None)
            return self.create_tree(root), self.create_tree(right_tree)
        else:
            left_tree = root.l
            self.set_parent(child=left_tree, parent=None)
            root.l = None

            return self.create_tree(left_tree), self.create_tree(root)

    def insert(self, nev_el):
        self.n += 1
        new_root = Node(val=nev_el)
        tree_l, tree_r = self.split(nev_el)

        if tree_l:
            left_root = tree_l.root
            new_root.l = left_root
            left_root.parent = new_root
        if tree_r:
            right_root = tree_r.root
            new_root.r = right_root
            right_root.parent = new_root
        self.upgrate_h(new_root)
        self.root = new_root

    def upgrate_h(self, node_x: Node) -> None:
        '''Обновление высоты родителя, при учете, что дерево снизо корректное'''
        h_list = [0, 0]
        if node_x.l is not None:
            h_list[0] = node_x.l.h
        if node_x.r is not None:
            h_list[1] = node_x.r.h

        node_x.h = max(h_list) + 1
        node_x.diff = h_list[1] - h_list[0]

    def __str__(self):
        if self.n == 0:
            return str(None)
        parent = [self.root]
        ans = [[self.root]]
        while parent != []:
            childs = []
            for p in parent:
                if p is not None:
                    childs += [p.l, p.r]
            ans.append(childs)
            parent = []
            for c in childs:
                if c is not None and c not in parent:
                    parent += [c]

        for line in ans:
            for i, x in enumerate(line):
                if i % 2 == 0 and i != 0:
                    print("\t", end='')
                if x:
                    print(f"{x} (diff={x.diff}) (parent={x.parent})(h={x.h}) childs=({x.l}, {x.r})", end=" ")
                else:
                    print(f"{x} (0)", end=" ")
            print()
        return ""

    def splay_smaller(self):
        start = self.root
        if start is not None:
            while start.l is not None:
                start = start.l
            return self.splay(start)
        return start

    def merge(self, tree_l, tree_r):
        if tree_l is None:
            return tree_r
        if tree_r is None:
            return tree_l

        tree_r.splay_smaller()
        main_root = tree_r.root
        main_root.l = tree_l.root
        self.set_parent(tree_l.root, main_root)
        return self.create_tree(main_root)

    def extract(self, val):
        self.n -= 1
        if self.find(val):
            if self.root:
                self.set_parent(self.root.l, None)
                self.set_parent(self.root.r, None)
                tree_l = self.create_tree(self.root.l)
                tree_r = self.create_tree(self.root.r)
                new_tree =  self.merge(tree_l, tree_r)
                if new_tree:
                    self.root = new_tree.root
                    self.upgrate_h(self.root)
                else:
                    self.root = None


def test_splay_tree(treesize=990, iters=990):
    """Just a simple test harness to demonstrate the speed of
    splay trees when a few items are searched for very frequently."""
    # Build a binary tree and a splay tree
    print("Building trees")
    bintree = ClassicBinaryTree()
    spltree = SplayTree()
    x = [i for i in range(0, treesize)]
    for n in x:
        bintree.insert(n)
        spltree.insert(n)
    print("Done building")
    searches = x[-20:]

    # Search the splay tree 1000 times
    t1 = time.time()
    for i in range(0, iters):
        for n in searches:
            node = spltree.find(n)
            if (node == None):
                print("ERROR: %d" % n)
    t2 = time.time()
    print("Searched for 20 items %dx in splay tree: %.1f sec" % (iters, t2 - t1))

    # Search the binary tree 1000 times
    t1 = time.time()
    for i in range(0, iters):
        for n in searches:
            node = bintree.find(n)
            if (node == None):
                print("ERROR: %d" % n)
    t2 = time.time()
    print("Searched for 20 items %dx in binary tree: %.1f sec" % (iters, t2 - t1))

if __name__ == '__main__':
    from ClassicBinaryTree import ClassicBinaryTree
    import time

    test_splay_tree()



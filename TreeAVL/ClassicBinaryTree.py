import datetime


class Node:
    def __init__(self, val, parent=None, l=None, r=None, h=0, diff=0):
        '''Узел дерева
            val - значение узла
            l - левый ребенок
            r - правый ребенок
            h - высота поддерева
        '''
        self.val = val
        self.parent = parent
        self.r = r
        self.l = l
        self.h = h
        self.diff = diff

    def __str__(self):
        return f"{self.val}"


class ClassicBinaryTree:
    '''Классическое дерево поиска'''

    def __init__(self):
        self.root = None
        self.n = 0

    def create_root(self, val: int):
        '''Создание корня дерева'''
        if self.n == 0:
            self.root = Node(val=val)
            self.n += 1


    def find_place(self, find_val: int, node: Node = None, flag_del=False):
        '''
        Находим место для изменения значения или поика элемета
        :param find_val: Значение поиска
        :param node: текущий узел
        :param flag_del: Флаг (bool) для удаление узла
        :return: Node - Узел дерева, flag - левая/правая
        '''
        now_node = node or self.root
        val_node = now_node.val
        ans = None, None
        if find_val == val_node:
            # усли есть такое значение, то вернет его
            if flag_del:
                self.go_extract(now_node)
                self.balance(now_node)
                return None, None
            return now_node, None
        elif find_val < val_node:
            if now_node.l is None:
                return now_node, "left"
            ans = self.find_place(find_val, now_node.l, flag_del=flag_del)
        else:
            if now_node.r is None:
                # если нет , то вернет его
                return now_node, "right"
            ans = self.find_place(find_val, now_node.r, flag_del=flag_del)
        self.upgrate_h(now_node)
        return ans

    def find(self, find_val: int) -> bool:
        '''
        Поиск значение, отвечает на вопрос есть ли в мно-ве такой эл-т
        :param find_val:
        :return: bool
        '''
        place_node, flag = self.find_place(find_val)
        if flag:
            return True
        return False

    def upgrate_h(self, node_x: Node) -> None:
        '''Обновление высоты родителя, при учете, что дерево снизо корректное'''
        h_list = [0, 0]
        if node_x.l is not None:
            h_list[0] = node_x.l.h
        if node_x.r is not None:
            h_list[1] = node_x.r.h

        node_x.h = max(h_list) + 1
        node_x.diff = h_list[1] - h_list[0]

    def new_element(self, parent, new_val: int) -> None:
        '''Создание нового элемента по значению'''
        new_node = Node(new_val)
        new_node.parent = parent
        self.n += 1
        return new_node

    def insert(self, new_val: int, node: Node = None):
        '''
        Добавить новый элемент
        :param new_val: Значение нового эл-та
        :param node: текущий узел
        :return: bool
        '''

        self.create_root(new_val)
        now_node = node or self.root
        val_node = now_node.val
        if new_val == val_node:
            # если такой элемент уже есть, то добавлять его нельзя
            return False
        elif new_val < val_node:
            if now_node.l is None:
                # Если нет левого ребенка, то нашли его место
                new_node = self.new_element(now_node, new_val)
                new_node.h = 1
                now_node.l = new_node

            else:
                # Если есть, то идем глубже в левого ребенка                          
                self.insert(new_val, now_node.l)
        else:
            if now_node.r is None:
                # Если нет правого ребенка, то нашли его место
                new_node = self.new_element(now_node, new_val)
                new_node.h = 1
                now_node.r = new_node
            else:
                # Если есть, то идем глубже в правого ребенка
                self.insert(new_val, now_node.r)
        self.balance(now_node)


    def balance(self, now_node):

        self.upgrate_h(now_node)
        pass

    def compare_to_parent(self, node):
        '''Сравнение клбчей родителя и узла'''
        parent = node.parent
        if parent is None:
            return None
        print(parent.val , node.val)
        return bool(parent.val < node.val)

    def del_node(self, node):
        '''Удаление ссылок, у узла node'''
        node.parent = None
        node.l = None
        node.r = None

    def go_extract(self, node_del: Node) -> None:
        '''
        Удаление элемента
        :param val: значение, которое хотим удалить
        :return: None
        '''
        self.n -= 1
        parent = node_del.parent
        delta = self.compare_to_parent(node_del)
        # Случай 1: У удаляемого узла нет левого ребенка.
        if node_del.l is None:
            if parent is None:
                # удаление корня
                self.root = node_del.r
                if self.root is not None:
                    self.root.parent = None
            else:

                if delta > 0:
                    parent.l = node_del.r
                    if parent.l is not None:
                        node_del.r.parent = parent
                else:
                    parent.r = node_del.r
                    if parent.r is not None:
                        node_del.r.parent = parent
        else:
            left_person = node_del.l
            if left_person.r is None:
                # Случай 2: У удаляемого узла есть  левый ребенок, у которого, в свою очередь нет правого ребенка.
                parent_node_del = node_del.parent
                if delta is None:
                    # удаление корня
                    self.root = left_person
                    self.root.parent = None
                    r_child = node_del.r
                    self.root.r = r_child
                    if r_child is not None:
                        r_child.parent = self.root
                    l_child = self.root.l
                    if l_child is not None:
                        l_child.parent = self.root

                else:
                    if delta > 0:
                        # Левый сын
                        parent_node_del.l = left_person
                    elif delta < 0:
                        parent_node_del.r = left_person
                    left_person.parent = parent_node_del
                self.del_node(node_del)
            else:
                # Случай 3: У удаляемого узла есть левый ребенок, у которого есть правый ребенок.
                right_person = left_person
                while right_person.r != None:
                    right_person = left_person.r
                node_del.val = right_person.val  # копируем значение у самого правого ребенка (большое) в левом дереве
                parent_right_person = right_person.parent
                parent_right_person.r = right_person.l
                right_person.l = None
                parent_right_person.r = None

    def extract(self, val):
        '''
        Удаление узла по значению val
        '''
        self.find_place(val, flag_del=True)

    def __str__(self):
        now_time = datetime.datetime.now()
        end_time = now_time + datetime.timedelta(seconds=5)

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
            # print([f'x={x} p={p} l={x.l} r={x.r}' for x in parent])


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


if __name__ == '__main__':
    tree = ClassicBinaryTree()
    for x in range(5):
        tree.insert(x)
    for x in range(-1, -6, -1):
        tree.insert(x)
    tree.extract(0)
    print(tree)


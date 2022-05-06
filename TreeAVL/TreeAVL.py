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


class ClassicTreeAVL:
    '''Классическое дерево поиска'''

    def __init__(self):
        self.root = None
        self.n = 0

    def create_root(self, val: int):
        '''Создание корня дерева'''
        if self.n == 0:
            self.root = Node(val=val)
            self.n += 1
            return True
        return False

    def find_place(self, find_val: int, node: Node = None, flag_del=False):
        '''
        Находим место для изменения значения или поика элемета
        :param find_val: Значение поиска
        :param node: текущий узел
        :return: Node - Узел дерева, flag - левая/правая
        '''
        now_node = node or self.root
        val_node = now_node.val
        ans = None, None
        if find_val == val_node:
            # усли есть такое значение, то вернет его
            print(flag_del)
            if flag_del:
                print("!")
                self.go_extract(find_val, now_node)
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
        if self.create_root(new_val):
            return
        now_node = node or self.root
        val_node = now_node.val
        if new_val == val_node:
            # если такой элемент уже есть, то добавлять его нельзя
            return False
        elif new_val < val_node:
            if now_node.l is None:
                # Если нет левого ребенка, то нашли его место
                new_node = self.new_element(now_node, new_val)
                now_node.l = new_node
            else:
                # Если есть, то идем глубже в левого ребенка                          
                self.insert(new_val, now_node.l)
        else:
            if now_node.r is None:
                # Если нет правого ребенка, то нашли его место
                new_node = self.new_element(now_node, new_val)
                now_node.r = new_node
            else:
                # Если есть, то идем глубже в правого ребенка
                self.insert(new_val, now_node.r)
        # TODO Балансировка!
        self.upgrate_h(now_node)

    def del_root(self, node_root):
        print(f"уДАЛАЯЕМ  {node_root.val}")
        if node_root.l is None:
            node_root.r = None
            return
        left_person = node_root.l

        while left_person.r != None:
            left_person = left_person.r
        parent_left_person = left_person.parent
        self.root.val = left_person.val
        parent_left_person.r = None


    def go_extract(self, val, node_del: Node) -> None:
        '''
        Удаление элемента
        :param val: значение, которое хотим удалить
        :return:
        '''
        print(node_del.val, "!!!!")
        parent = node_del.parent

        if node_del.l is None:
            if parent is None:
                #удаление корня
                self.root = node_del.r
                self.root.parent = None
            else:
                if parent.val > val:
                    parent.l = node_del.r
                    if parent.l is not None:
                        node_del.r.parent = parent
                else:
                    parent.r = node_del.r
                    if parent.r is not None:
                        node_del.r.parent = parent
        else:
            left_person = node_del.l
            while left_person.r != None:
                left_person = left_person.r
            node_del.val = left_person.val  #копируем значение у самого большого в левом дереве
            parent_left_person = left_person.parent
            #TODO ЕРУНДА КАКАЯ-ТО
            parent_left_person.r = left_person.l
            if left_person.l is not None:
                left_person.l.parent = parent_left_person
            left_person.l = None
            left_person.parent = None
            if left_person.l is None and left_person.r is None:
                if parent_left_person.val == parent_left_person.l.val:
                    parent_left_person.l = None
                    print("!!!!")
    def extract(self, val):
        print("extract")
        self.find_place(val, flag_del=True)

    def __str__(self):
        parent = [self.root]
        ans = [[self.root]]
        while parent != []:
            childs = []
            for p in parent:
                childs += [p.l, p.r]
            ans.append(childs)
            parent = []
            for c in childs:
                if c is not None:
                    parent += [c]

        for line in ans:
            for i, x in enumerate(line):
                if i % 2 == 0 and i != 0:
                    print("\t", end='')
                if x:
                    print(f"{x} (parent={x.parent})(h={x.h}) childs=({x.l}, {x.r})", end=" ")
                else:
                    print(f"{x} (0)", end=" ")
            print()
        return ""


if __name__ == '__main__':
    tree = ClassicTreeAVL()
    tree.insert(10)
    tree.insert(5)
    tree.insert(0)
    tree.insert(7)
    tree.insert(15)
    print(tree)
    tree.extract(10)
    print()
    print(tree)
    tree.extract(5)
    print()
    print(tree)
    tree.extract(7)
    print()
    print(tree)
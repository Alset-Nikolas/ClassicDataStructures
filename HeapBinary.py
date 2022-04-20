'''
 Струтура данных: Куча
 Добавить элемент в структуру данных. ~ O(logN)
 Извлечь из структуры данных наибольший (вариант - наименьший) элемент. Извлеченный элемент удаляется из структуры ~ O(log(N))
 Неоптимальный вариант.
'''


class HeapElement:
    '''
    Элемент кучи, состоит из
    val - значения
    parent - ссылка на родителя
    left_person, right_person - ссылки на детей
    '''

    def __init__(self, val, parent):
        self.val = val
        self.parent = parent
        self.left_person = None
        self.right_person = None

    def __str__(self):
        return f"{self.val}"


class Heap:
    '''
    root - корень
    n - кол-во эл-ов
    '''

    def __init__(self):
        self.root = None
        self.n = 0

    def get_obj(self, m) -> HeapElement:
        '''
        Функция возвращает m-ый обьект
        '''
        parent = self.get_obg_parent(m)
        if m % 2 == 0:
            return parent.left_person
        return parent.right_person

    def get_obg_parent(self, m: int) -> HeapElement:
        '''
            Функция возвращает родителя m-го обьекта
        '''
        parents = self.get_rout_parent(m)
        obj = self.root
        for parent in parents:
            if parent % 2 == 0:
                obj = obj.left_person
            else:
                obj = obj.right_person
        return obj

    def get_rout_parent(self, m: int)-> list[int]:
        '''
            Функция возвращает путь от корня до родителя m
        :param m:
        :return:
        '''
        if m // 2 == 0:
            last_el = 1
        else:
            last_el = m // 2
        parents_rout = []
        while last_el != 1:
            parents_rout.append(last_el)
            last_el //= 2
        return parents_rout[::-1]

    def check_up(self, new_el: HeapElement) -> None:
        '''
        Протаскивание new_el до своей позиции
        :param new_el:
        :return:
        '''
        parent = new_el.parent
        if parent is None:
            return
        if parent.val < new_el.val:
            parent.val, new_el.val = new_el.val, parent.val
            self.check_up(parent)
        return

    def find_my_position(self, parent: HeapElement, val: int) -> None:
        '''
        Какой будет ребенок левый или правый
        :param parent:
        :param val:
        :return:
        '''
        if parent.left_person is None:
            parent.left_person = HeapElement(val=val, parent=parent)
            self.check_up(parent.left_person)
        else:
            parent.right_person = HeapElement(val=val, parent=parent)
            self.check_up(parent.right_person)

    def append(self, val: int) -> None:
        '''Добавить новый элемент со значением val'''
        if self.n == 0:
            self.n += 1
            self.root = HeapElement(val=val, parent=None)
            return
        self.n += 1
        my_parent = self.get_obg_parent(self.n)
        self.find_my_position(parent=my_parent, val=val)
    def __str__(self):
        self.pprint(self.root)
        return ""

    def pprint(self, element: HeapElement) -> None:
        '''
        Вывести дерево
        :param element:
        :return:
        '''
        if element is None:
            return
        print(f"{element}:  L={element.left_person} R={element.right_person}")
        self.pprint(element=element.left_person)
        self.pprint(element=element.right_person)

    def check_down(self, start_obj):
        '''
        Поправляем дерево, после удаление сверху
        :param start_obj:
        :return:
        '''
        if start_obj is None:
            return
        left = start_obj.left_person
        right = start_obj.right_person
        if left is not None or right is not None:
            if (right is None and left is not None) or (right.val and left.val and left.val > right.val):
                if left.val is not None and left.val > start_obj.val:
                    left.val, start_obj.val = start_obj.val, left.val
                    self.check_down(left)
            else:
                if right is not None and right.val > start_obj.val:
                    right.val, start_obj.val = start_obj.val, right.val
                    self.check_down(right)
        return

    def get_Max(self) -> int:
        '''
        Возвращает максимальное значение в куче, т.е корень
        :return:
        '''
        res = self.root.val
        last_obj = self.get_obj(m=self.n)
        self.n -= 1
        if last_obj is None:
            self.root = None
        else:
            self.root.val = last_obj.val
            parent = last_obj.parent
            if parent.left_person.val == last_obj.val:
                parent.left_person = None
            elif parent.right_person.val == last_obj.val:
                parent.right_person = None
            self.check_down(self.root)
        return res


if __name__ == '__main__':
    numbers = [10, 1, 4, 21, 120, 12, 3, 123, 12565]
    a = Heap()
    for x in numbers:
        a.append(x)
    print(f"Куча для списка {numbers}")
    print("=" * 100)
    print(a)
    print("=" * 100)
    print("Вывод максимального элемента ")
    for x in range(a.n):
        print(f"x= {a.get_Max()}")
    new = 10
    a.append(new)
    print("=" * 100)
    print(f"Добавим {new}")
    print(a)


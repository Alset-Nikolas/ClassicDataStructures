class СellList:
    def __init__(self, index, value, next_cell=None):
        self.__value = value
        self.__next_cell = next_cell
        self.index = index

    def get_value(self):
        return self.__value

    def next(self):
        return self.__next_cell

    def put(self, new_value):
        self.__value = new_value

    def new_link(self, link):
        self.__next_cell = link

    def __str__(self):
        return f"{self.__value}"

class LinkedList:

    def __init__(self):
        self.len_list = 0
        self.first_cell = None
        self.end_cell = None

        self.index_iter = 0

    def append(self, value):
        '''добавление элемента в конец списка'''
        new_index = self.len_list
        new_cell = СellList(value=value, next_cell=None, index=new_index)
        self.len_list += 1
        if self.first_cell is None:
            self.first_cell = new_cell
            self.end_cell = self.first_cell
            return
        self.end_cell.new_link(new_cell)
        self.end_cell = new_cell

    def get(self, i):
        '''получение элемента по индексу'''
        cell = self.first_cell
        for x in range(self.len_list):
            if cell.index == i:
                return cell
            cell = cell.next()

    def remove(self, i):
        '''удаление элемента по индексу'''
        cell = self.first_cell
        cell_del = None
        cell_before_del = None
        for x in range(self.len_list):
            if cell.index == i:
                cell_del = cell
            if cell_del is None:
                cell_before_del = cell
            else:
                cell.index -= 1
            cell = cell.next()
        if cell_del.next() is not None:
            cell_before_del.new_link(link=cell_del.next())
        else:
            cell_before_del.new_link(link=None)
        self.len_list -= 1


    def __str__(self):
        txt = "["
        cell = self.first_cell
        for x in range(self.len_list):
            txt += str(cell)
            if x != self.len_list-1:
                txt += ", "
            cell = cell.next()
        txt += ']'
        return txt

    def __iter__(self):
        self.index_iter = 0
        return self

    def __next__(self):
        cell = self.first_cell
        for x in range(self.len_list):
            if cell.index == self.index_iter:
                break
            cell = cell.next()
        while self.index_iter < self.len_list:
            if cell.index == self.index_iter:
                self.index_iter += 1
                return cell
        raise StopIteration

if __name__ == '__main__':

    my_list = LinkedList()
    my_list.append(10)
    my_list.append(20)
    my_list.append(30)
    print('Текущий список:')
    print(my_list)
    print('Получение третьего элемента:')
    print(my_list.get(2))
    print('Удаление второго элемента.')
    my_list.remove(1)
    print('Новый список:')
    print(my_list)

    for x in my_list:
        print(x, end=" ")

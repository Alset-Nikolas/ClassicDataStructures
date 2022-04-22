import math


def pprint(mass):
    n = len(mass)
    h = 0
    while n != 0:
        n //= 2
        h += 1
    info = []
    start_i = 0
    n = 0
    for x in range(h):
        len_ = 2 ** h * len(str(mass[0]))
        probel = len_ // (2 ** n + 1)
        text = []
        for x in range(2 ** n):
            text.append(" " * probel)
            if start_i < len(mass):
                text.append(str(mass[start_i]))
                start_i += 1
            else:
                break
        text.append(" " * probel)
        info.append("".join(text))

        n += 1
    print("\n".join(info))


'''

Классическая бинарная куча:
        insert (Добавить элемент)-> O(Log(N))
        get_max (взять максимум с кучи (не удалять его))-> O(Log(N))
        pop_max (удалить корень и перестроить кучу)- > O(Log(N))
        build_heap (построить кучу)-> 0(N*Log(N))
        decrease_key (увеличить элемент i в куче)-> O(Log(N))
        heap_sort (сортировка)-> 
            T:O(N*Log(N))
            M:O(2*N)=0(N)
        heap_optimal_sort (сортировка)->
            T:O(N*Log(N))
            M:O(N)
        erase_t (удалить по значению value)-> O(Log(N))
'''


class HeapBineryClassic:
    def __init__(self, heap_del=None):
        self.heap_list = []
        self.heap_size = 0
        self.pointer_list = []  # Указатель на вершину x в куче
        self.num_id = []  # Индификатор соот вершине x
        self.heap_del = heap_del

    def exchange(self, i, j):
        k = self.num_id[i]
        m = self.num_id[j]
        self.num_id[i], self.num_id[j] = self.num_id[j], self.num_id[i]
        self.pointer_list[k], self.pointer_list[m] = self.pointer_list[m], self.pointer_list[k]
        self.heap_list[i], self.heap_list[j] = self.heap_list[j], self.heap_list[i]

    def is_life(self, i):
        return 0 <= i < self.heap_size

    def shift_up(self, i):
        parent = i // 2
        largest_person = parent
        if self.is_life(i) and self.heap_list[largest_person] < self.heap_list[i]:
            largest_person = i
            if largest_person != parent:
                self.exchange(i=i, j=parent)
                self.shift_up(parent)

    def shift_down(self, i):
        left_person_index = 2 * i + 1
        right_person_index = 2 * i + 2
        largest_person = i
        if self.is_life(left_person_index) and self.heap_list[largest_person] < self.heap_list[left_person_index]:
            largest_person = left_person_index
        if self.is_life(right_person_index) and self.heap_list[largest_person] < self.heap_list[right_person_index]:
            largest_person = right_person_index
        if largest_person != i:
            self.exchange(i=i, j=largest_person)
            self.shift_down(largest_person)

    def build_heap(self, mass):
        self.heap_list = mass.copy()
        self.heap_size = len(mass)
        self.num_id = list(range(self.heap_size))
        self.pointer_list = list(range(self.heap_size))
        for i in range(self.heap_size // 2, -1, -1):
            self.shift_down(i)

    def get_heap(self):
        return self.heap_list

    def get_max(self):
        if self.heap_del is None:
            return self.heap_list[0]
        while self.heap_del.get_max() == self.get_max():
            self.heap_del.pop_max()
            self.pop_max()
        return self.heap_list[0]

    def decrease_key(self, i, val):
        index_real = self.pointer_list[i]
        self.heap_list[index_real] -= val
        if val > 0:
            self.shift_up(i)
        else:
            self.shift_down(i)

    def insert(self, x):
        if self.heap_size < len(self.heap_list):
            self.heap_list[self.heap_size] = x
        else:
            self.heap_list.append(x)
            self.heap_size += 1
        self.shift_up(self.heap_size)

    def extract_max(self):
        self.exchange(i=0, j=self.heap_size - 1)
        self.shift_down(0)

    def pop_max(self):
        self.extract_max()
        self.heap_list.pop()
        self.heap_size -= 1

    def heap_sort(self):
        new_list = []
        for x in range(heap.heap_size):
            new_list.append(heap.get_max())
            heap.pop_max()
        return new_list

    def heap_optimal_sort(self):
        for i in range(len(self.heap_list)):
            self.extract_max()
            self.heap_size -= 1
        return self.heap_list

    def erase_t(self, i):
        '''Удаление по индификатору t - по счету в изначальном списке '''
        t = self.pointer_list[i]
        if self.is_life(t):
            self.heap_list[t] = math.inf
            self.shift_up(t)
            self.pop_max()

    def erase(self, val):
        self.heap_del.insert(val)


if __name__ == '__main__':
    heap = HeapBineryClassic()
    mass = [0, 0, 9, 5, 23, 0, 0, 2, 2, 1, 4, 0, 12, -1, 0]
    print(f"mass={mass}")
    print("=" * 100)
    heap.build_heap(mass)
    print(f"Куча:")
    pprint(heap.get_heap  ())
    print(f"Сортировка (легкая версия) =  {heap.heap_sort()}")
    print(f"Куча сейчас ")
    pprint(heap.get_heap())
    print("Добавим старые элементы")
    heap.build_heap([0, 0, 9, 5, 23, 0, 0, 2, 2, 1, 4, 0, 12, -1, 0])
    print(f"Сортировка (сложная версия) reverse=True =  {heap.heap_optimal_sort()}")


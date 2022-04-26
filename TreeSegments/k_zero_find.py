#Задача:
#K-ый ноль на отрезке
#есть mass =[a0, a1, a2, .. ,an-1] - из 0/1
#Есть несколько типов запросов
#       1. update в точке a[pos] = val
#       2. c l-ый по r-ый элемент нужно найти k-ый ноль [l, r] --> k0
#Теперь будем хранить кол-во нулей на отрезке

#                         33
#                27             5
#         10           17       5
#     3      7    8       9     5
#   1   2   3   4   4   4   5   5
#   |   |   |   |   |   |   |   |
#   0   0   0   0   1   1   0   0
import math


class SegmentItem:
    def __init__(self, val, left_segment, right_segment):
        self.val = val
        self.left_segment = left_segment
        self.right_segment = right_segment

    def __str__(self):
        return f"val={self.val} l={self.left_segment} r={self.right_segment}"


class TreeSegments:
    '''Сумма на отрезке'''

    def __init__(self, mass):
        self.mass = mass.copy()
        self.n = len(self.mass)
        self.h = math.ceil(math.log2(self.n))
        self.tree = []
        self.tree_el = 0
        self.calc_all_elements()
        self.index_first_leaf = 0

    def calc_all_elements(self):
        '''O(n*Log(n))'''
        for i in range(self.h + 1):
            self.index_first_leaf = (1 << i)
            self.tree_el += self.index_first_leaf
        self.tree = [SegmentItem(0, None, None) for x in range(self.tree_el)]
        self.index_first_leaf -= 1
        self.fill_tree()

    def fill_tree(self):
        '''O(n*Log(n))'''
        for i in range(self.index_first_leaf, self.index_first_leaf + self.n):
            self.tree[i].val = self.mass[i - self.index_first_leaf]
            self.tree[i].left_segment = i - self.index_first_leaf
            self.tree[i].right_segment = i - self.index_first_leaf + 1
            parent_index = (i - 1) >> 1  # //2
            while parent_index != 0:
                self.tree[parent_index].val += self.tree[i].val
                if self.tree[parent_index].left_segment is None:
                    self.tree[parent_index].left_segment = self.tree[i].left_segment
                else:
                    self.tree[parent_index].left_segment = min(self.tree[parent_index].left_segment,
                                                               self.tree[i].left_segment)

                if self.tree[parent_index].right_segment is None:
                    self.tree[parent_index].right_segment = self.tree[i].right_segment
                else:
                    self.tree[parent_index].right_segment = max(self.tree[parent_index].right_segment,
                                                                self.tree[i].right_segment)

                parent_index = (parent_index - 1) >> 1  # //2

            self.tree[0].val += self.tree[i].val

        self.tree[0].left_segment = 0
        self.tree[0].right_segment = self.n

    def get_sum(self, l, r, start_index=0):
        '''O(Log(n))'''
        v = self.tree[start_index]
        tl = v.left_segment
        tr = v.right_segment
        if tl == l and tr == r:
            return v.val
        tm = (tl + tr) >> 1
        ans = 0
        if l <= tm:
            child_index = 2 * start_index + 1
            ans += self.get_sum(l=l, r=min(r, tm), start_index=child_index)
        if r >= tm + 1:
            child_index = 2 * start_index + 2
            ans += self.get_sum(l=max(l, tm), r=r, start_index=child_index)
        return ans

    def update(self, position, delta):
        '''O(Log(n))'''
        self.tree[position + self.index_first_leaf].val = -delta
        self.mass[position] -= delta
        parent_index = (position + self.index_first_leaf - 1) >> 1
        while parent_index != 0:
            self.tree[parent_index].val -= delta
            parent_index = (parent_index - 1) >> 2
        self.tree[0].val -= delta



if __name__ == '__main__':
    mass = [0, 0, 0, 0, 1, 1, 0, 0]
    k = 2
    l = 3
    r = 8
    for i in range(len(mass)):
        if mass[i] == 0:
            mass[i] = 1
        else:
            mass[i] = 0

    tree = TreeSegments(mass)
    m = tree.get_sum(l=0, r=l)
    start = 0
    find = m + k
    def go(start, find):
        if find > tree.tree_el[2*start+1]:
            find -= tree.tree_el[2*start+1]
            start = 2*start + 2
            return go(start, find)
        elif find < tree.tree_el[2*start+1]:
            start = 2*start + 1
            return go(start, find)

        if find < tree.tree_el[2*start+2]:
            start = 2*start + 2
        else:


    print(mass)


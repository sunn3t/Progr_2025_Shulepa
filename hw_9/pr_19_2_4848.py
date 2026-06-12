class Heap:
    def __init__(self):
        self.mItems = [0]
        self.mSize = 0
    def empty(self):
        return len(self.mItems) == 1
    def insert(self, key):
        self.mSize += 1
        self.mItems.append(key)
        self.siftUp()
    def siftUp(self):
        i = len(self.mItems) - 1
        while i > 1:
            parent = i // 2
            if self.mItems[i] < self.mItems[parent]:
                self.swap(parent, i)
            else:
                break
            i = parent
    def extractMinimum(self):
        root = self.mItems[1]
        self.mItems[1] = self.mItems[-1]
        self.mItems.pop()
        self.mSize -= 1
        if self.mSize > 0:
            self.siftDown()
        return root
    def siftDown(self):
        i = 1
        while (2 * i) <= self.mSize:
            left = 2 * i
            right = 2 * i + 1
            min_child = self.minChild(left, right)
            if self.mItems[i] > self.mItems[min_child]:
                self.swap(min_child, i)
            else:
                break
            i = min_child
    def swap(self, i, j):
        self.mItems[i], self.mItems[j] = self.mItems[j], self.mItems[i]
    def minChild(self, left_child, right_child):
        if right_child > self.mSize:
            return left_child
        if self.mItems[left_child] < self.mItems[right_child]:
            return left_child
        return right_child

if __name__=='__main__':
    lst = list(map(int, input().split()))
    heap = Heap()
    for x in lst:
        heap.insert(x)
    result = []
    while not heap.empty():
        result.append(str(heap.extractMinimum()))
    print(" ".join(result))
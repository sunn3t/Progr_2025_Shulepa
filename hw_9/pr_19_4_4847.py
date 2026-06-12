class Heap:
    def __init__(self):
        self.mItems = [0]
        self.mSize = 0
        self.positions = {}
    def swap(self, i, j):
        self.mItems[i], self.mItems[j] = self.mItems[j], self.mItems[i]
        self.positions[self.mItems[i][0]] = i
        self.positions[self.mItems[j][0]] = j
    def siftUp(self, i):
        while i > 1:
            parent = i // 2
            if self.mItems[i][1] > self.mItems[parent][1]:
                self.swap(i, parent)
                i = parent
            else:
                break
    def siftDown(self, i):
        while 2 * i <= self.mSize:
            left = 2 * i
            right = 2 * i + 1
            max_child = left
            if right <= self.mSize and self.mItems[right][1] > self.mItems[left][1]:
                max_child = right
            if self.mItems[i][1] < self.mItems[max_child][1]:
                self.swap(i, max_child)
                i = max_child
            else:
                break
    def insert(self, id_, priority):
        self.mItems.append([id_, priority])
        self.mSize += 1
        self.positions[id_] = self.mSize
        self.siftUp(self.mSize)
    def pop(self):
        top_id, top_pr = self.mItems[1]
        self.swap(1, self.mSize)
        self.positions.pop(top_id)
        self.mItems.pop()
        self.mSize -= 1
        if self.mSize > 0:
            self.siftDown(1)
        return top_id, top_pr
    def change(self, i, new):
        j = self.positions[i]
        old = self.mItems[j][1]
        self.mItems[j][1] = new
        if new > old:
            self.siftUp(j)
        else:
            self.siftDown(j)

if __name__=='__main__':
    heap = Heap()
    f = open('input.txt')
    for line in f.readlines():
        cmd = line.split()
        if cmd[0] == "ADD":
            heap.insert(cmd[1], int(cmd[2]))
        elif cmd[0] == "POP":
            id_, pr = heap.pop()
            print(id_, pr)
        elif cmd[0] == "CHANGE":
            heap.change(cmd[1], int(cmd[2]))
    f.close()
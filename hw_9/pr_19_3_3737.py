class Heap:
    def __init__(self):
        self.mItems = [0]
        self.mSize = 0
    def insert(self, key):
        self.mItems.append(key)
        self.mSize += 1
    def check(self):
        for i in range(1, self.mSize + 1):
            left = 2 * i
            right = 2 * i + 1
            if left <= self.mSize:
                if self.mItems[i] > self.mItems[left]:
                    return False
            if right <= self.mSize:
                if self.mItems[i] > self.mItems[right]:
                    return False
        return True
if __name__=='__main__':
    n = int(input())
    lst = list(map(int, input().split()))
    heap = Heap()
    for x in lst:
        heap.insert(x)
    if heap.check():
        print("YES")
    else:
        print("NO")
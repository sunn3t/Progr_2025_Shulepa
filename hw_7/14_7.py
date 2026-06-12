class Node:

    def __init__(self, item):
        self.item = item
        self.next: Node | None = None


class Queue:

    def __init__(self):
        self._front: Node | None = None
        self._back: Node | None = None
        self._size = 0

    def empty(self):
        return self._front is None

    def push(self, item):
        node = Node(item)
        if self.empty():
            self._front = node
        else:
            self._back.next = node
        self._back = node
        self._size += 1
        return "ok"

    def pop(self):
        if self.empty():
            return "error"
        item = self._front.item
        self._front = self._front.next
        self._size -= 1
        return item

    def front(self):
        if self.empty():
            return "error"
        return self._front.item

    def size(self):
        return self._size

    def clear(self):
        self.__init__()
        return "ok"

    def exit(self):
        return "bye"
if __name__=='__main__':
    n=int(input())
    l1=list(map(int,input().split()))
    l2=list(map(int,input().split()))
    a,b=Queue(),Queue()
    for i in range(n//2):
        a.push(l1[i])
        b.push(l2[i])
    cnt=0

    while not a.empty() and not b.empty() and cnt<=200000:
        cnt+=1
        e1,e2=a.pop(),b.pop()
        if (e1!=0 or e2!=n-1) and (e1!=n-1 or e2!=0):
            if e1>e2:
                a.push(e1)
                a.push(e2)
            else:
                b.push(e1)
                b.push(e2)
        else:
            if e1==0:
                a.push(e1)
                a.push(e2)
            else:
                b.push(e1)
                b.push(e2)
    if a.empty() or b.empty():
        if a.empty():
            print('second', cnt)
        else:
            print('first',cnt)
    else:
        print('draw')
import sys

sys.setrecursionlimit(50000)


class Node:

    def __init__(self, data: int):
        self.data: int = data
        self.next: [Node | None] = None
        self.back = None


class List:

    def __init__(self):
        self.first = None
        self.last = None

    def addToTail(self, val: int) -> None:
        node = Node(val)
        if self.first == None:
            self.first = node
            self.last = node
            return
        node.back = self.last
        self.last.next = node
        self.last = node
        return

    def Print(self) -> None:
        node = self.first
        while node != None:
            print(node.data, end=' ')
            node = node.next
        print()
        return

    def ReorderList(self) -> None:
        if self.first == None:
            # print('b')
            return
        elif self.first.next == None:
            # print('a')
            return
        elif self.first.next.next == None:
            return
        l = List()
        l.first = self.first.next
        l.last = self.last.back
        l.first.back, l.last.next = None, None

        l.ReorderList()

        self.first.next = self.last
        self.last.back = self.first

        self.last.next = l.first
        l.first.back = self.last
        self.last = l.last
        return


if __name__ == '__main__':
    l = List()
    n = int(input())
    ll = list(map(int, input().split()))
    for i in ll:
        l.addToTail(i)
    l.ReorderList()
    l.Print()
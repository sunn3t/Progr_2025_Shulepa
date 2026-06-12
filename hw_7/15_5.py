class Node:

    def __init__(self, data: int):
        self.data: int = data
        self.next: [Node | None] = None


class List:

    def __init__(self):
        self.head: [Node | None] = None
        self.tail: [Node | None] = None

    def addToTail(self, val: int) -> None:
        node = Node(val)
        if self.head == None:
            self.head = node
            return
        if self.tail == None:
            self.head.next = node
            self.tail = node
            return
        self.tail.next = node
        self.tail = node
        return

    def Print(self) -> None:
        node = self.head
        while node != None:
            print(node.data, end=' ')
            node = node.next
        print()
        return

    def PrintReverse(self) -> None:
        if self.head.next == None:
            print(self.head.data, end=' ')
            return
        l = List()
        l.head = self.head.next
        l.tail = self.tail
        l.PrintReverse()
        print(self.head.data, end=' ')


if __name__ == '__main__':
    l = List()
    n = int(input())
    ll = list(map(int, input().split()))
    for i in ll:
        l.addToTail(i)
    l.Print()
    l.PrintReverse()
class Node:

    def __init__(self, item):
        self.item = item
        self.next: Node | None = None
        self.back = None


class Queue:

    def __init__(self):
        self._front: Node | None = None
        self._back: Node | None = None
        self._size = 0

    def empty(self):
        return self._size == 0

    def push_back(self, item):
        node = Node(item)
        if self.empty():
            self._front = node
            self._back = node
        else:
            self._back.next = node
            node.back = self._back
        self._back = node
        self._size += 1
        return "ok"

    def push_front(self, item):
        node = Node(item)
        if self.empty():
            self._front = node
            self._back = node
        else:
            self._front.back = node
            node.next = self._front
        self._front = node
        self._size += 1
        return "ok"

    def pop_back(self):
        if self.empty():
            return "error"
        item = self._back.item
        self._back = self._back.back
        try:
            self._back.next = None
        finally:
            self._size -= 1
            return item

    def pop_front(self):
        if self.empty():
            return "error"
        item = self._front.item
        self._front = self._front.next
        try:
            self._front.back = None
        finally:
            self._size -= 1
            return item

    def front(self):
        if self.empty():
            return "error"
        return self._front.item

    def back(self):
        if self.empty():
            return "error"
        return self._back.item

    def size(self):
        return self._size

    def clear(self):
        self.__init__()
        return "ok"

    def exit(self):
        return "bye"

    def execute(self, cmd: str):
        method, *args = cmd.split()
        return getattr(self, method)(*args)


if __name__ == '__main__':
    queue = Queue()
    f = open("input.txt")
    for line in f:
        result = queue.execute(line)
        print(result)
        if result == "bye":
            break
    f.close()
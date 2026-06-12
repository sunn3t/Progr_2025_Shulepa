class Node:
    def __init__(self, item):
        self._item = item
        self._next = None


class Stack:

    def __init__(self):
        self._top = None
        self._size = 0

    def empty(self):
        return self._size == 0

    def push(self, n):
        new_node = Node(n)
        new_node._next = self._top
        self._top = new_node
        self._size += 1
        return "ok"

    def pop(self):
        if self.empty():
            return 'error'
        res = self.back()
        self._top = self._top._next
        self._size -= 1
        return res

    def back(self):
        if self.empty():
            return 'error'
        return self._top._item

    def size(self):
        return self._size

    def clear(self):
        self._top = None
        self._size = 0
        return "ok"

    def exit(self):
        return "bye"

    def execute(self, cmd: str):
        method, *args = cmd.split()
        return getattr(self, method)(*args)


if __name__ == '__main__':
    stack = Stack()
    f = open("input.txt")
    for line in f:
        result = stack.execute(line)
        print(result)
        if result == "bye":
            break
    f.close()

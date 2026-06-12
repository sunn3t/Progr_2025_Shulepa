class PrefixTree:
    def __init__(self):
        self.children = {}

    def get_child(self, i):
        return self.children[i]

    def has_child(self, i):
        return i in self.children

    def add_child(self, i):
        self.children[i] = PrefixTree()

    def is_leaf(self):
        return len(self.children) == 0

    def add(self, phone):
        i = 0
        node = self
        while i < len(phone) and node.has_child(phone[i]):
            node = node.get_child(phone[i])
            i += 1
        if i == len(phone):
            return False
        while i < len(phone):
            node.add_child(phone[i])
            node = node.get_child(phone[i])
            i += 1
        return True

    def dfs(self, name, s=''):
        self.children = dict(sorted(self.children.items()))
        print(s + name)
        for i in self.children.keys():
            self.children[i].dfs(i, s=s + ' ')


if __name__ == '__main__':
    tree = PrefixTree()
    n = int(input())
    for _ in range(n):
        lst = list(input().split('\\'))
        result = tree.add(lst)
    tree.children = dict(sorted(tree.children.items()))
    for i in tree.children.keys():
        tree.children[i].dfs(i)

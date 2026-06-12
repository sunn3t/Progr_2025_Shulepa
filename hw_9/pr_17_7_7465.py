class SearchTree:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

    def insert(self, key):
        if key < self.key:
            if self.left is None:
                self.left = SearchTree(key)
            else:
                self.left.insert(key)
        else:
            if self.right is None:
                self.right = SearchTree(key)
            else:
                self.right.insert(key)

    def same(self, tree):
        if tree is None:
            return 0
        if self.key != tree.key:
            return 0
        if self.left is None and tree.left is not None:
            return 0
        if self.left is not None and tree.left is None:
            return 0
        if self.right is None and tree.right is not None:
            return 0
        if self.right is not None and tree.right is None:
            return 0
        left_same = 1
        right_same = 1
        if self.left is not None:
            left_same = self.left.same(tree.left)
        if self.right is not None:
            right_same = self.right.same(tree.right)
        return left_same and right_same


n = int(input())
lst1 = list(map(int, input().split()))
m = int(input())
lst2 = list(map(int, input().split()))
tree1 = SearchTree(lst1[0])
for x in lst1[1:]:
    tree1.insert(x)
tree2 = SearchTree(lst2[0])
for x in lst2[1:]:
    tree2.insert(x)
print(int(tree1.same(tree2)))
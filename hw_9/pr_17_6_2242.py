class BinaryTree:
    def __init__(self, item=None, left=None, right=None):
        self.mItem = item
        self.mLeftChild = None
        self.mRightChild = None
        if left is not None:
            self.setLeft(left)
        if right is not None:
            self.setright(right)
    def empty(self):
        return self.mItem is None
    def item(self):
        if not self.empty():
            return self.mItem
    def setNode(self, item):
        if isinstance(item, BinaryTree):
            self.mItem = item.item()
            self.mLeftChild = item.leftChild()
            self.mRightChild = item.rightChild()
        else:
            self.mItem = item
    def hleft(self):
        return self.mLeftChild is not None
    def hasRight(self):
        return self.mRightChild is not None
    def hasNoChildren(self):
        return self.mLeftChild is None and self.mRightChild is None
    def leftChild(self):
        return self.mLeftChild
    def rightChild(self):
        return self.mRightChild
    def leftItem(self):
        if self.hleft():
            return self.mLeftChild.item()
    def rightItem(self):
        if self.hasRight():
            return self.mRightChild.item()
    def removeLeft(self):
        self.mLeftChild = None
    def removeRight(self):
        self.mRightChild = None
    def setLeft(self, item):
        if isinstance(item, BinaryTree):
            self.mLeftChild = item
        elif self.hleft():
            self.mLeftChild.setNode(item)
        else:
            self.mLeftChild = BinaryTree(item)
    def setright(self, item):
        if isinstance(item, BinaryTree):
            self.mRightChild = item
        elif self.hasRight():
            self.mRightChild.setNode(item)
        else:
            self.mRightChild = BinaryTree(item)

def line(tree):
    if tree is None:
        return ""
    return (tree.item()+line(tree.leftChild())+line(tree.rightChild()))
if __name__=='__main__':
    lst=[]
    while True:
        s = input().strip()
        if s == '*':
            break
        lst.append(s)
    tree = BinaryTree()
    for i in range(len(lst)-1,-1,-1):
        for j in range(len(lst[i])-1,-1,-1):
            value = lst[i][j]
            if tree.empty():
                tree.setNode(value)
                continue
            curr = tree
            while True:
                if value < curr.item():
                    if curr.hleft():
                        curr = curr.leftChild()
                    else:
                        curr.setLeft(value)
                        break
                else:
                    if curr.hasRight():
                        curr = curr.rightChild()
                    else:
                        curr.setright(value)
                        break
    print(line(tree))
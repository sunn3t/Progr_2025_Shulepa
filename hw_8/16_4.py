from collections import deque
class Tree:
    def __init__(self, key):
        self.key=key
        self.val=0
        self.children=[]
        self.parent=None
    def bfs_search(self,f):
        m=None
        queue=deque()
        queue.append((self,self.val))
        while len(queue)>0:
            node,vall=queue.popleft()
            if len(node.children)==0:
                if m==None:
                    m=vall
                else:
                    m=f(m,vall)
            for child in node.children:
                queue.append((child,vall+child.val))
        return m
    def bfs(self, key, came_frome=None):
        queue=deque()
        queue.append(self)
        while len(queue)>0:
            node=queue.popleft()
            if node.key==key:
                return node
            if node is came_frome:
                continue
            for child in node.children:
                queue.append(child)
        return None
    def add(self, parent_key, childe_key):
        parent=self.bfs(parent_key)
        if parent is None:
            raise RuntimeError
        node=Tree(childe_key)
        node.parent=parent
        parent.children.append(node)
    def add_val(self, key, val):
        node=self.bfs(key)
        node.val=val
        return 0
    def reset(self, key, nw):
        nw=self.bfs(nw)
        node=self.bfs(key)
        nw.children.append(node)
        self.children.remove(node)
        return
if __name__=='__main__':
    tree=Tree(0)
    n=int(input())
    for i in range(1,n+1):
        tree.add(0,i)
    for i in range(1,n+1):
        val, m, *args=map(int, input().split())
        tree.add_val(i,val)
        if m==0:
            continue
        for j in args:
            tree.reset(j,i)
    print(tree.bfs_search(min))
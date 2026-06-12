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
        self.add(nw,key)
        self.children.remove(self.bfs(key))
    def dfs(self, step=0):
        s=set()
        step+=1
        for i in self.children:
            i.dfs(step=step)
            s.update([i.val])
        if -1 in s and 1 in s:
            if step%2==0:
                self.val=-1
            else:
                self.val=1
        elif -1 in s and 0 in s:
            if step%2==0:
                self.val=-1
            else:
                self.val=0
        elif 1 in s and 0 in s:
            if step%2==0:
                self.val=0
            else:
                self.val=1
        elif len(s)==1:
            self.val=list(s)[0]
        return self.val
if __name__=='__main__':
    tree=Tree(1)
    n=int(input())
    for i in range(2,n+1):
        tree.add(1,i)
    for i in range(2,n+1):
        t, p, *w=input().split()
        tree.reset(i,int(p))
        if t=='L':
            tree.add_val(i,int(w[0]))
    tree.dfs()
    res=tree.val
    if res==1:
        res='+'+str(1)
    print(res)

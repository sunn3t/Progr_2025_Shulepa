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

    def execute(self, cmd: str):
        method, *args = cmd.split()
        return getattr(self, method)(*args)
def wave(graph, start,distances):
    q = Queue()
    for i in distances.keys():
        q.push(i)
    while not q.empty():
        current = q.pop()
        for neighbour in graph[current]:
            if neighbour not in distances:
                q.push(neighbour)
                distances[neighbour] = distances[current] + 1
            if len(distances)==len(graph):
                return distances
    return distances

if __name__=='__main__':
    n,m=map(int,input().split())
    graph=[]
    for i in range(n):
        graph.append([])
    for i in range(m):
        a,b=map(int,input().split())
        graph[a-1].append(b-1)
        graph[b-1].append(a-1)
    k=int(input())
    distances={}
    l=list(map(int,input().split()))
    for i in range(k):
        distances[l[i]-1]=0
        #graph[l[0]-1]=graph[l[0]-1]+graph[l[i]-1]
    dct=wave(graph,l[0]-1,distances)
    res=l[0]-1
    for i in dct.keys():
        if dct[i]>dct[res]:
            res=i
        elif dct[i]==dct[res]:
            res=min(i,res)
    #print(distances)
    print(dct[res],res+1,sep='\n')
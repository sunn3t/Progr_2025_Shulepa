def deep(st,fn,d,D,use,graph):
    use[st]=1
    cnt=0
    if d>D:
        use[st]=0
        return 0
    if st==fn:
        use[fn]=0
        return 1
    for i in graph[st]:
        if use[i]==0:
            cnt=cnt+deep(i,fn,d+1,D,use,graph)
    use[st]=0
    return cnt
if __name__=='__main__':
    n,k,a,b,d=map(int,input().split())
    graph=[]
    for i in range(n):
        l=[]
        graph.append(l)
    for i in range(k):
        q,w=map(int,input().split())
        graph[q-1].append(w-1)
    use=[0]*n
    print(deep(a-1,b-1,0,d,use,graph))


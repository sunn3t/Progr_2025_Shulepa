import sys
sys.setrecursionlimit(100001)
def dfs(start,graph,stack,use):
    if use[start] == 1:
        print(-1)
        exit(0)
    use[start]=1
    for v in graph[start]:
        if use[v]!=2:
            dfs(v,graph, stack,use)
    use[start]=2
    stack.append(start+1)

if __name__=='__main__':
    n,m=map(int,input().split())
    graph=[]
    for i in range(n):
        graph.append([])
    for i in range(m):
        a,b=map(int,input().split())
        graph[a-1].append(b-1)
    use=[0]*n
    stack=[]
    for i in range(n):
        if use[i]==0:
            dfs(i,graph,stack,use)
    print(*(stack[::-1]))
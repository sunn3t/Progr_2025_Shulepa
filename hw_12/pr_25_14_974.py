import sys
INF = sys.maxsize
if __name__=='__main__':
    n=int(input())
    graph=[]
    dist=[]
    for i in range(n):
        ll=list(map(int,input().split()))
        graph.append(ll)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                graph[i][j]=min(graph[i][j],graph[i][k]+graph[k][j])
    for i in graph:
        print(*i)
if __name__=='__main__':
    n=int(input())
    graph=[]
    for i in range(n):
        l=list(map(int,input().split()))
        graph.append(l)
    cnt=0
    for i in range(n):
        if sum(graph[i])==1:
            cnt+=1
    print(cnt)